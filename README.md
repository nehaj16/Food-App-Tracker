# Food Tracker

A mobile app for keeping track of what food I have, what's about to expire, and what I could cook with it. The goal is simple: waste less food and stay consistent with my eating goals.

## What it does

Every grocery run gets logged as individual items. If I bought chicken thighs two weeks ago and again today, those are two separate entries, each with its own quantity, unit, and expiry date (for example, 10 lb of chicken in the freezer). The app always surfaces whatever is closest to expiring, so the decision of what to cook next basically makes itself.

Down the line, it will scan grocery receipts to log items automatically and use AI to suggest meals based on what's actually in the kitchen.

## Tech stack

- **Mobile app:** React Native
- **API:** FastAPI with Pydantic
- **Database:** PostgreSQL
- **AI:** LLM-based meal suggestions and shelf-life estimates
- **OCR:** Google Vision for receipt scanning

## Roadmap

**Stage 1: Core backend (in progress)**
Postgres schema, full CRUD API for inventory and ingredients, smart deduplication so "Chicken" and "chicken" resolve to the same ingredient, and type-ahead search.

**Stage 2: Expiry intelligence**
Automatic shelf-life estimates (asked once, cached forever) and priority sorting so the most urgent items rise to the top.

**Stage 3: Mobile app**
React Native app with the inventory list, add/edit flows, and filters by location (fridge, freezer, cabinet).

**Stage 4: AI meal suggestions**
Top 3 meal ideas built strictly from what's on hand, prioritizing ingredients that are about to expire.

**Stage 5: Receipt scanning**
Snap a photo of a receipt, review what it found, confirm, done.

**Stage 6: Cook flow**
Pick a meal, check off what you used, and the inventory updates itself.

**Someday:** meal history, nutrition tracking, multi-user support.

## Getting started

git clone git@github.com:YOUR_USERNAME/food-tracker.git
cd food-tracker/backend

# setup instructions coming as the backend lands
