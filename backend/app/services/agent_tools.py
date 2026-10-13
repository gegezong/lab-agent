from datetime import datetime
import json
from sqlalchemy.orm import Session
from langchain_core.tools import tool

from app.common.exceptions import BusinessException
from app.models.equipment import Equipment
from app.models.reservation import Reservation
from app.models.user import User
from app.services import equipment_service, kb_service, lab_service, reservation_service


def build_tools(db: Session, current_user: User):

    @tool
    def search_lab_docs(query: str) -> str:
        """根据用户的提问检索知识库"""
        try:
            return kb_service.search(query) or "没有检索到相关的资料"
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)

    @tool
    def list_open_labs(keywords: str = "") -> str:
        """查询开放的实验室列表"""
        try:
            keywords = keywords.strip() or None
            page = lab_service.get_lab_page_list(
                db, page=1, page_size=10, keywords=keywords, status=1
            )
            rows = [
                {
                    "id": item.id,
                    "name": item.name,
                    "location": item.location,
                    "capacity": item.capacity,
                    "open_time": item.open_time,
                    "close_time": item.close_time,
                }
                for item in page.list
            ]
            return json.dumps({"total": page.total, "labs": rows}, ensure_ascii=False)
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)

    @tool
    def search_equipments(keywords: str) -> str:
        """按设备名称关键字在全部实验室中查询设备，并返回设备所在实验室信息。适合回答“哪些实验室有某设备”。"""
        try:
            keywords = keywords.strip()
            if not keywords:
                return json.dumps(
                    {"ok": False, "error": "请提供设备名称关键字"},
                    ensure_ascii=False,
                )
            items = (
                db.query(Equipment)
                .filter(Equipment.name.ilike(f"%{keywords}%"))
                .order_by(Equipment.id.desc())
                .limit(20)
                .all()
            )
            rows = []
            for item in items:
                lab = item.lab
                rows.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "spec": item.spec,
                        "quantity": item.quantity,
                        "status": item.status,
                        "lab_id": item.lab_id,
                        "lab_name": lab.name if lab else None,
                        "lab_location": lab.location if lab else None,
                        "lab_open_time": lab.open_time if lab else None,
                        "lab_close_time": lab.close_time if lab else None,
                        "lab_status": lab.status if lab else None,
                    }
                )
            return json.dumps(
                {"total": len(rows), "equipments": rows}, ensure_ascii=False
            )
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)

    @tool
    def list_lab_equipments(lab_id: int, keywords: str = "") -> str:
        """根据已知实验室 ID 查询该实验室下的设备列表，可用设备名称关键字筛选。"""
        try:
            keywords = keywords.strip() or None
            page = equipment_service.get_equipment_page_list(
                db, page=1, page_size=10, lab_id=int(lab_id), keywords=keywords
            )
            rows = [
                {
                    "id": item.id,
                    "name": item.name,
                    "lab_id": item.lab_id,
                    "lab_name": item.lab_name,
                    "sepc": item.spec,
                    "quantity": item.quantity,
                    "status": item.status,
                }
                for item in page.list
            ]
            return json.dumps(
                {"total": page.total, "equipments": rows}, ensure_ascii=False
            )
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)

    @tool
    def create_lab_reservation(
        lab_id: int,
        date: str,
        start_time: str,
        end_time: str,
        equipment_id: int | None = None,
        remark: str | None = None,
    ) -> str:
        """创建预约单预约实验室或设备"""
        try:
            data = Reservation(
                lab_id=lab_id,
                equipment_id=equipment_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                remark=remark,
            )
            reservation_service.create_reservation(db, current_user, data)
            return json.dumps(
                {
                    "ok": True,
                    "message": "预约已提交，请等待管理员审核",
                    "lab_id": lab_id,
                    "equipment_id": equipment_id,
                    "date": date,
                    "start_time": start_time,
                    "end_time": end_time,
                },
                ensure_ascii=False,
            )
        except BusinessException as exc:
            return json.dumps({"ok": False, "error": exc.message}, ensure_ascii=False)
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)

    @tool
    def get_today() -> str:
        """获取服务器当前的日期  2026-09-20"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d")

    return [
        search_lab_docs,
        list_open_labs,
        search_equipments,
        list_lab_equipments,
        create_lab_reservation,
        get_today,
    ]
