import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.db.models import MenuItem, RestaurantInfo, Reservation

async def init_db():
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    # Load restaurant data
    with open("data/res-bot-dataset.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize collections
    menu_items = db.menu_items
    restaurant_info = db.restaurant_info
    reservations = db.reservations
    
    # Clear existing data
    await menu_items.delete_many({})
    await restaurant_info.delete_many({})
    await reservations.delete_many({})
    
    # Insert menu items
    menu_documents = []
    for category in data.get('menu', {}).get('categories', []):
        category_name = category.get('name', '')
        for item in category.get('items', []):
            # Create dietary tags from boolean flags
            dietary_tags = []
            if item.get('vegetarian', False):
                dietary_tags.append('vegetarian')
            if item.get('vegan', False):
                dietary_tags.append('vegan')
            if item.get('gluten_free', False):
                dietary_tags.append('gluten-free')
                
            menu_item = MenuItem(
                name=item['name'],
                description=item['description'],
                price=float(item['price']),
                category=category_name,
                dietary_tags=dietary_tags,
                is_available=True
            )
            menu_documents.append(menu_item.model_dump(by_alias=True))
    
    if menu_documents:
        await menu_items.insert_many(menu_documents)
        print(f"Inserted {len(menu_documents)} menu items")
    
    # Insert restaurant information
    restaurant_data = data.get('restaurant', {})
    hours = {}
    for day, time in restaurant_data.get('hours', {}).items():
        hours[day] = f"{time.get('open')} - {time.get('close')}"
    
    # Process special events
    special_events = []
    
    # Happy hour
    happy_hour = data.get('menu', {}).get('specials', {}).get('happy_hour', {})
    if happy_hour:
        special_events.append({
            "name": "Happy Hour",
            "description": ", ".join(happy_hour.get('offers', [])),
            "times": happy_hour.get('times', ''),
            "days": happy_hour.get('days', [])
        })
    
    # Weekly specials
    weekly_specials = data.get('menu', {}).get('specials', {}).get('weekly_specials', [])
    for special in weekly_specials:
        special_events.append({
            "name": special.get('name', ''),
            "description": special.get('description', ''),
            "days": special.get('valid_days', [])
        })
    
    # Create restaurant info document
    restaurant = RestaurantInfo(
        name=restaurant_data.get('name', ''),
        description=restaurant_data.get('about', ''),
        address=f"{restaurant_data.get('address', {}).get('street', '')}, {restaurant_data.get('address', {}).get('city', '')}, {restaurant_data.get('address', {}).get('state', '')} {restaurant_data.get('address', {}).get('zip', '')}",
        phone=restaurant_data.get('contact', {}).get('phone', ''),
        email=restaurant_data.get('contact', {}).get('email', ''),
        opening_hours=hours,
        special_events=special_events
    )
    await restaurant_info.insert_one(restaurant.model_dump(by_alias=True))
    print("Inserted restaurant information")
    
    # Create indexes
    await menu_items.create_index("category")
    await menu_items.create_index("dietary_tags")
    await reservations.create_index("user_id")
    await reservations.create_index("date")
    
    print("Database initialization completed")

if __name__ == "__main__":
    asyncio.run(init_db()) 