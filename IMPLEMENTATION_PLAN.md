# F1 Undercut Strategy Analysis - Implementation Plan

## Project Overview
End-to-end web application analyzing whether undercut strategy in Formula 1 is worthwhile (2022-2024 seasons). Includes data pipeline, Power BI dashboards, and a 3D racing-themed website.

---

## Phase 1: Project Structure & Setup

### Directory Structure
```
f1-undercut-analysis/
├── data/                          # Data and notebooks
│   ├── notebooks/
│   │   ├── 01_data_fetch.ipynb   # FastF1 API data collection
│   │   ├── 02_data_processing.ipynb
│   │   ├── 03_undercut_analysis.ipynb
│   │   └── 04_power_bi_export.ipynb
│   ├── raw/                       # Raw data from FastF1
│   └── processed/                 # Cleaned and processed data
├── database/
│   ├── schema.sql                 # Database schema
│   └── migrations/                # Supabase migrations
├── website/                       # Frontend application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   ├── utils/
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── power-bi/                      # Power BI report files
│   └── f1_undercut_analysis.pbix
├── docs/
│   ├── README.md                  # Project overview
│   ├── DATA_PIPELINE.md           # Data collection process
│   ├── ANALYSIS_FINDINGS.md       # Results and insights
│   └── DEPLOYMENT.md              # How to run/deploy
└── .gitignore
```

---

## Phase 2: Data Pipeline (Python Jupyter Notebooks)

### Notebook 1: Data Fetch (01_data_fetch.ipynb)
**Purpose**: Collect F1 data from FastF1 API for 2022-2024

**Tasks**:
- Install fastf1 library
- Fetch race data for 2022, 2023, 2024 seasons
- Extract pit stop information
- Extract lap time data
- Extract driver and team information
- Save raw data to CSV/Parquet

**Key Data Points**:
- Race details (circuit, date, weather conditions)
- Driver information (driver name, team, number)
- Lap data (lap number, time, position, compound, stint)
- Pit stop data (lap, driver, time lost, new compound)

### Notebook 2: Data Processing (02_data_processing.ipynb)
**Purpose**: Clean and structure data for analysis

**Tasks**:
- Handle missing/invalid data
- Standardize formats
- Aggregate lap times by stint
- Calculate tire degradation
- Identify pit stop windows
- Structure data for database import

### Notebook 3: Undercut Analysis (03_undercut_analysis.ipynb)
**Purpose**: Calculate undercut strategy metrics

**Key Metrics to Calculate**:
1. **Undercut Identification**:
   - Detect when driver A pits earlier than driver B (normally ahead)
   - Track if A gains track position due to pit strategy

2. **Success Metrics**:
   - Position gain/loss from undercut attempt
   - Time advantage gained
   - Driver pairs where undercut was attempted
   - Success rate by circuit, driver, team

3. **Comparative Analysis**:
   - Undercut vs. Overcut outcomes
   - Undercut vs. Track position maintenance
   - Tire compound impact on undercut success

4. **Advanced Metrics**:
   - Average gap closed by undercut
   - Undercut effectiveness by circuit type (street/permanent)
   - Team strategy comparison
   - Driver-specific undercut success rates
   - Lap position change analysis

5. **Statistical Analysis**:
   - Confidence intervals on success rates
   - Correlation between undercut and final position
   - Track-specific patterns

### Notebook 4: Power BI Export (04_power_bi_export.ipynb)
**Purpose**: Prepare data for Power BI dashboard

**Tasks**:
- Format data for Power BI import
- Create aggregated views
- Generate summary statistics
- Export to CSV/database

---

## Phase 3: Database Design (Supabase PostgreSQL)

### Core Tables

#### 1. `seasons` table
```
- id (PK)
- year (2022, 2023, 2024)
```

#### 2. `races` table
```
- id (PK)
- season_id (FK)
- name (circuit name)
- date
- country
- circuit_type (street/permanent)
- lap_distance
- total_laps
```

#### 3. `drivers` table
```
- id (PK)
- number
- name
- first_name
- last_name
- country
```

#### 4. `teams` table
```
- id (PK)
- name
- country
```

#### 5. `race_results` table
```
- id (PK)
- race_id (FK)
- driver_id (FK)
- team_id (FK)
- starting_position
- final_position
- points
```

#### 6. `lap_data` table
```
- id (PK)
- race_id (FK)
- driver_id (FK)
- lap_number
- lap_time (seconds)
- position
- compound (SOFT/MEDIUM/HARD/INTERMEDIATE/WET)
- stint_number
```

#### 7. `pit_stops` table
```
- id (PK)
- race_id (FK)
- driver_id (FK)
- lap
- stop_duration (seconds)
- new_compound
- stop_number
```

#### 8. `undercut_events` table
```
- id (PK)
- race_id (FK)
- driver_id_undercut (FK) - driver attempting undercut
- driver_id_target (FK) - driver being undercut
- undercut_lap
- position_before
- position_after
- gap_before (seconds)
- gap_after (seconds)
- successful (BOOLEAN)
- time_gain (seconds)
```

#### 9. `undercut_analysis_summary` table
```
- id (PK)
- race_id (FK)
- circuit_name
- total_undercut_attempts
- successful_attempts
- success_rate (%)
- avg_gap_closed (seconds)
- avg_time_gained (seconds)
```

---

## Phase 4: Website (3D Racing-Themed Frontend)

### Tech Stack
- **Framework**: React + Vite
- **3D Graphics**: Three.js or Babylon.js
- **Styling**: Tailwind CSS + custom racing theme
- **Power BI**: Power BI Embedded SDK
- **Data Fetching**: React Query + Supabase client
- **UI Library**: Custom + racing-themed components

### Website Pages

1. **Home/Landing Page**
   - 3D animated racing scene
   - Quick statistics (undercut success rate, top circuits, etc.)
   - CTA to dashboard

2. **Main Dashboard**
   - Embedded Power BI dashboard
   - Key metrics overview
   - Interactive filters

3. **Detailed Analysis Page**
   - Circuit-by-circuit breakdown
   - Driver comparisons
   - Team strategies

4. **Data Explorer**
   - Interactive race data browser
   - Pit stop timeline visualization
   - Lap time comparisons

5. **About/Documentation**
   - GitHub repo link
   - Methodology explanation
   - Data sources

### Design Elements
- **Colors**: Racing red (#DC0000), black (#000000), white (#FFFFFF), accent silver (#C0C0C0)
- **Typography**: Bold, modern fonts (Michroma, Orbitron for F1 feel)
- **3D Elements**:
  - Animated formula car on landing
  - Circuit track visualization
  - Data point animations
  - Particle effects for racing theme

### Key Components
- Navigation bar (sticky, racing-themed)
- Hero section with 3D car model
- Stats cards with animations
- Power BI dashboard embed
- Data visualization components
- Footer with GitHub/documentation links

---

## Phase 5: Power BI Dashboard

### Dashboard Sheets

1. **Executive Summary**
   - Overall undercut success rate
   - Key findings
   - Top circuits for undercut
   - Best undercut drivers

2. **Circuit Analysis**
   - Undercut success by circuit
   - Circuit characteristics impact
   - Street vs. Permanent comparison

3. **Driver Performance**
   - Driver-specific undercut stats
   - Team-based analysis
   - Pairwise driver matchups

4. **Tactical Analysis**
   - Tire strategy effectiveness
   - Pit window analysis
   - Time gain/loss distributions

5. **Comparative Analysis**
   - Undercut vs. Overcut outcomes
   - Undercut vs. Status quo (no pit strategy)
   - Success factors correlation

---

## Phase 6: GitHub Documentation

### README.md
- Project overview
- Quick start guide
- Key findings summary
- Technologies used

### DATA_PIPELINE.md
- How to run Jupyter notebooks
- Data sources (FastF1 API)
- Data processing steps
- Database schema explanation

### ANALYSIS_FINDINGS.md
- Detailed findings
- Metrics explanations
- Key insights
- Statistical significance

### DEPLOYMENT.md
- How to deploy website
- Environment setup
- Power BI embedding guide
- Database setup instructions

---

## Implementation Sequence

### Week 1-2: Data Pipeline
1. Set up Jupyter environment
2. Implement data fetch notebook
3. Implement data processing
4. Implement undercut analysis

### Week 3: Database & Backend
1. Design and create Supabase schema
2. Load processed data into database
3. Verify data integrity
4. Create Power BI data export

### Week 4-5: Frontend Website
1. Set up React + Vite project
2. Build 3D racing homepage
3. Create dashboard pages
4. Embed Power BI dashboards
5. Style with racing theme

### Week 6: Polish & Documentation
1. Complete GitHub documentation
2. Add deployment guides
3. Final testing and optimization
4. Publishing

---

## Key Technologies

### Data Pipeline
- Python 3.9+
- FastF1 library
- Pandas, NumPy
- Jupyter Notebook

### Database
- Supabase (PostgreSQL)
- Row-Level Security policies

### Frontend
- React 18+
- Vite
- Three.js / Babylon.js
- Tailwind CSS
- Power BI Embedded

### Deployment
- Vercel/Netlify (website)
- GitHub Pages (documentation)
- Supabase (database)

---

## Success Criteria

✓ Data pipeline successfully collects 2022-2024 F1 data
✓ Database contains clean, normalized data
✓ Undercut metrics accurately calculated
✓ Power BI dashboards embedded and functional
✓ Website is 3D racing-themed and visually impressive
✓ All analysis documented on GitHub
✓ Clear answer: "Is undercut strategy worth it?"

