Architecture Diagram
---
<img width="619" height="332" alt="Screenshot 2026-02-18 at 5 40 37 PM" src="https://github.com/user-attachments/assets/28ca80a1-9371-45f0-957d-eed8b003f18b" />

Subscription Detection Flowchart
---
<img width="272" height="1039" alt="Subscription Detection Flowchart" src="https://github.com/user-attachments/assets/830c8e11-be08-4106-bfab-921d70d14e3c" />

Component Breakdown
---
Front-end: 

- UI - index.html
- Upload Button
- Subscription display
  
Back-end: 

- Upload API - POST
- CSV processing
- Temporary File Storage
- Subscription detection algorithm
- Export and Integration

Interfaces
---
Flask Server - Frontend-Backend communication

POST /upload - file upload API

POST /get - Index/Homepage

Data Model:

- Monthly transactional CSVs 
- CSV Schema:{Date, Amount, Category, Service, Billing Interval, Merchant Name, Subscription ID}
Temporarily hold CSV files during runtime and automatic deletion after processing

Key Tradeoffs and Decisions
---

- Settling on front end being minimalist and not too “extra” 
- Flask serving both html and API endpoints through app.py
- Not to implement storage on the backend and deleting everything after it passes through
- Strict formatting for the sake of simplicity IE: CSV only, category, amount, date etc… 

Risks and Mitigation
---
- Risk: False positives in subscription detection
  - Mitigation: Setting specific parameters on the backend to identity if it’s a subscription or daily purchase

- Risk: Different banks have different csv formats
  - Mitigation: Creating various types of mapping in order to match formatted data

