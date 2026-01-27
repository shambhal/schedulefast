from sqlalchemy import event
from sqlalchemy.orm import Session
from  models.category import Order,OrderHistory,OrderItem,Book
from datetime import datetime
@event.listens_for(Order, "after_update")
def order_success(mapper, connection, target):
    """
    Triggered when an Order is updated. If status becomes COMPLETE,
    it creates or updates related Book entries and adds an OrderHistory entry.
    """
    # Check if the order is COMPLETE
    if target.status!= "COMPLETE":
        return

    session = Session(bind=connection)
    try:
        # Fetch order items
        oitems = session.query(OrderItem).filter_by(order_id=target.id).all()
        order_info=session.query(Order).filter_by(Order.id==target.id).first()
        #if(order_info.status!='P')
        flag = True
        for oitem in oitems:
            existing_book = session.query(Book).filter_by(order_item_id=oitem.id).first()

            if not existing_book :
                book = Book(
                    dated=oitem.dated,
                    slot=oitem.slot,
                    status="BOOKED",
                    user_id=target.user_id,
                    order_item_id=oitem.id,
                    order_id=target.id,
                    #service_id=oitem.service_id,
                    email=target.email,
                    desc=oitem.name,
                    name=target.name,
                    phone=target.phone
                )
                session.add(book)
            else:
                existing_book.status = "BOOKED"
                session.add(existing_book)

        # Create order history entry
        oh = OrderHistory(
            dated=datetime.now().date,
            order_id=target.id,
            status="COMPLETED" if flag else "Partially Completed"
        )
        session.add(oh)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Order success processing failed: {e}")
    finally:
        session.close()