from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import db_helper
import generic_helper
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

inprogress_order = {}

@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()
        print("Received Payload:", payload)

        intent = payload['queryResult']['intent']['displayName']
        print("Intent:", intent)
        parameters = payload['queryResult'].get('parameters', {})
        output_contexts = payload['queryResult'].get('outputContexts', [])
        session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

        intent_handler_dict = {
            "Order Add - Context: Ongoing-order": add_to_order,
            "Track Order - Context : Ongoing Tracking": track_order,
            "Order Complete - Context: Ongoing-Order": complete_order,
            "Order Remove - Context: Ongoing-order": remove_from_order
        }

        if intent in intent_handler_dict:
            return await intent_handler_dict[intent](parameters, output_contexts, session_id)
        else:
            return JSONResponse(content={"fulfillmentText": f"No handler found for intent {intent}."})

    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(content={"fulfillmentText": f"An error occurred: {str(e)}"})


async def add_to_order(parameter: dict, output_contexts: list, session_id: str):
    food_item = parameter.get("Food_Item")
    quantities = parameter.get("number")

    print("Parsed food_item:", food_item)
    print("Parsed quantities:", quantities)

    if not food_item or not quantities or len(food_item) != len(quantities):
        fulfillment_text = "Sorry, I couldn't understand your request. Kindly mention the food item and quantity correctly."
    else:
        new_food_dict = dict(zip(food_item, quantities))

        if session_id in inprogress_order:
            current_food_dict = inprogress_order[session_id]
            current_food_dict.update(new_food_dict)
        else:
            inprogress_order[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_order[session_id])
        fulfillment_text = f"So far you have ordered: {order_str}. Do you need anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


async def remove_from_order(parameter: dict, output_contexts: list, session_id: str):
    print("Parameters received in remove_from_order:", parameter)

    if session_id not in inprogress_order:
        return JSONResponse(content={"fulfillmentText": "I am having trouble finding your order. Please try placing a new order."})

    current_order = inprogress_order[session_id]
    food_item = parameter.get("Food_Item") or parameter.get("food_item")

    if not food_item:
        return JSONResponse(content={"fulfillmentText": "Please mention the food item you want to remove."})

    removed_items = []
    no_such_item = []

    for item in food_item:
        item = item.strip().lower()
        matched_item = None

        for existing_item in list(current_order.keys()):
            if existing_item.lower() == item:
                matched_item = existing_item
                break

        if matched_item:
            del current_order[matched_item]
            removed_items.append(matched_item)
        else:
            no_such_item.append(item)

    if not current_order:
        del inprogress_order[session_id]

    response_parts = []

    if removed_items:
        response_parts.append(f"I have removed {', '.join(removed_items)} from your order.")
    if no_such_item:
        response_parts.append(f"I couldn't find {', '.join(no_such_item)} in your order.")

    if current_order:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        response_parts.append(f"Your current order is: {order_str}")
    elif not removed_items:
        response_parts.append("You have nothing in your order.")

    fulfillment_text = " ".join(response_parts).strip()

    return JSONResponse(content={"fulfillmentText": fulfillment_text or "Something went wrong while updating your order."})


async def complete_order(parameter: dict, output_contexts: list, session_id: str):
    if session_id not in inprogress_order:
        fulfillment_text = "I am having trouble finding your order. Please try placing a New Order."
    else:
        order = inprogress_order[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "I am having trouble saving your order. Please try again."
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Your order id is {order_id} and the amount to be paid is Rs. {order_total}. Thank you for ordering. We will deliver your food as soon as possible."

        del inprogress_order[session_id]

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


async def track_order(parameters: dict, output_contexts: list, session_id: str):
    order_id = parameters.get("order_id") or parameters.get("number")

    if not order_id:
        for context in output_contexts:
            if 'number' in context.get('parameters', {}):
                order_id = context['parameters']['number']
                break

    if not order_id:
        return JSONResponse(content={"fulfillmentText": "Order ID was not provided."})

    try:
        order_id = int(float(order_id))  # Handles float like 41.0
    except ValueError:
        return JSONResponse(content={"fulfillmentText": "Invalid Order ID format."})

    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id {order_id} is {order_status}."
    else:
        fulfillment_text = f"There is no order with order id: {order_id}."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "InProgress")
    return next_order_id

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    # Simple echo for now
    bot_reply = f"You said: {user_message} (this is a test reply)"
    return JSONResponse({"reply": bot_reply})