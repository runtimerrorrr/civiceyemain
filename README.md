# CivicEye — Citizen-Powered Civic Hazard Reporting System
### Visakhapatnam (Vizag), Andhra Pradesh, India

> **Tagline:** *See It. Report It. Fix It.*  
> **Jurisdiction:** Greater Visakhapatnam Municipal Corporation (GVMC) & Associated Civic Utilities

---

## 🏛️ Executive Summary

**CivicEye** is an open civic-tech web application designed for Visakhapatnam to empower citizens to document, map, and remediate urban infrastructure hazards. When citizens encounter road craters, open drainage chambers, illegal waste dumping, waterlogging, or dark streetlights across Vizag, CivicEye enables them to:

1. **Capture Visual & Geospatial Evidence:** Upload photographic proof and pinpoint the exact coordinates on an interactive OpenStreetMap centered on Visakhapatnam.
2. **Transparent Hazard Risk Heuristic:** Calculate hazard severity (**Low, Medium, High, or Critical**) using transparent, auditable rules based on pedestrian safety, traffic corridor exposure, and physical dimensions.
3. **Statutory Civic Complaint Generation:** Auto-draft a respectful, formal legal representation addressed to the competent GVMC / APEPDCL division, citing the Andhra Pradesh Municipal Corporations Act.
4. **Interactive City Surveillance Grid:** Explore hazards on a city-wide map with severity-colored custom SVG pins, filter by ward and category, track municipal remediation, and upvote community reports.

---

## 📍 Visakhapatnam MVP Demonstration Zones

CivicEye is calibrated specifically for Visakhapatnam with verified demo reports across key geographic sectors:

- **MVP Colony (Zone 2):** High-density residential & sports corridor (Sector 4, AS Raja Grounds, Shivaji Park).
- **Dwaraka Nagar (Zone 3):** City commercial center and interstate transit hub near RTC Complex.
- **Gajuwaka (Zone 5):** Commuter and heavy industrial zone along Kanithi Road and Old Gajuwaka.
- **Madhurawada (Zone 1):** Rapidly expanding IT SEZ corridor, Mithilapuri VUDA Colony, and NH16 service road.
- **Seethammadhara (Zone 2):** Educational & residential sectors including Balayya Sastri Layout.
- **Beach Road (Zone 3 Coastal):** Landmark promenade past INS Kursura Submarine Museum and Kailasagiri foothills.

---

## 🛠️ Technology Stack

| Layer | Technologies & Purpose |
|---|---|
| **Framework & Build** | React 18, TypeScript, Vite |
| **Styling & Aesthetics** | Tailwind CSS (Custom Civic Tech Palette: Deep Navy `#101D35`, Electric Blue `#3478F6`, Teal accents `#14B8A6`), Lucide Icons |
| **Mapping & Geospatial** | Leaflet 1.9, OpenStreetMap Standard Tiles, Custom SVG DivIcons |
| **Spatial Calculations** | Turf.js (distance calculations, nearest Vizag demonstration zone detection, cluster radius) |
| **Animations & Feedback** | Framer Motion & Canvas Confetti (celebratory feedback on report submission) |
| **Persistence** | LocalStorage service with isolated user report preservation during demo resets |
| **Ethics & AI Architecture**| Modular pluggable interface with transparent rule-based risk weighting; zero fabricated AI claims |

---

## 📄 Page Structure & Core Features

### 1. Home Page (`/`)
- **Hero:** "Your City. Your Eyes. Your Voice." with quick CTAs (*Report a Hazard* & *Explore Reports*).
- **Live Vizag Grid Preview:** Embedded interactive Leaflet mini-map displaying live reports across the city.
- **Real-Time Metrics:** Dynamic counters calculated from local storage records (*Total Logged, Critical Danger, Active, Resolved*).
- **Hazard Taxonomies:** Cards for Potholes, Open Manholes, Garbage Dumps, Waterlogging, Broken Streetlights, Damaged Footpaths, Fallen Trees, and Other civic defects.
- **3-Step Pipeline:** Visual walkthrough of Snap & Geotag &rarr; Risk Heuristic &rarr; Formal Complaint.
- **Recent Reports Carousel:** Real-time feed of newly filed observations.

### 2. Report a Hazard (`/report`)
- **Categorization:** Select from 8 standardized civic categories with department SLA indicators.
- **Photographic Upload:** Drag-and-drop dropzone with preview, removal, size validation, and **1-Click Test Presets** (Pothole, Manhole, Waterlog, Fallen Tree) for fast hackathon judging.
- **Interactive Leaflet Map:** Centered on Visakhapatnam `[17.6868, 83.2185]`. Click anywhere to drop or drag the coordinate pin.
- **GPS Integration:** "Use My Location" button with permission handling and fallback.
- **Auditable Severity Heuristic:** Transparently explains why a severity was assigned (potential injury, traffic exposure, dimensions, open manholes) with individual factor weights, allowing citizens to manually adjust ratings.
- **Reporter Details:** Optional name and contact for feedback, or 1-click anonymous reporting.
- **Success Celebration:** Generates unique tracking ID (e.g. `CE-VZG-2026-101`), fires confetti, and presents a complaint preview.

### 3. Hazard Registry & Dashboard (`/reports`)
- **Interactive OpenStreetMap Map:** Full-width Leaflet map with custom severity pins (critical pulsing rings, high amber pins, medium blue, low green).
- **Popup Previews:** Clicking any pin displays category, title, severity, date, and a direct button to the full report modal.
- **Search & Multi-Facet Filters:** Filter by category, severity risk, resolution status, and Vizag demonstration zone.
- **Dual View Layout:** Split map/card view on desktop, and a clean **Map vs. List toggle** on mobile.
- **Report Details Modal:** Complete inspection dialog featuring geotagged photo, risk factor breakdown, editable formal petition, resolution timeline tracker, and citizen upvoting.

### 4. About Us (`/about`)
- Comprehensive background on the urban infrastructure challenge in Indian cities.
- Project mission and expected public impact in Visakhapatnam.
- Detailed technical architecture table.
- Interactive FAQ addressing civic privacy, statutory petition drafting, and ethical AI disclosures.
- Explicit identification as a **Student Hackathon Prototype**.

---

## 🚦 How to Run the Application

### Prerequisites
- Node.js (v18 or higher) and npm installed on your system.

### 1-Click Windows Launch (Recommended)
Double-click `dev.bat` or run:
```bat
dev.bat
```
*(Automatically ensures Node.js is on PATH and starts the Vite development server at `http://localhost:5173`)*

### Manual Installation & Development Server
```bash
# 1. Navigate to the project root directory
cd civiceye

# 2. Install dependencies (if not already installed)
npm install

# 3. Start the Vite local development server
npm run dev
```

The application will be live at: **`http://localhost:5173`**

### Standalone Server
```bash
# Serves the compiled production build on port 5173
node serve.js
```

---

## 🗺️ Official GVMC Datasets Integrated

1. **98 Official GVMC Ward Boundaries (`public/data/gvmc_wards.geojson`):**
   - Extracted directly from official municipal GIS surveys containing all 98 administrative wards grouped across Zones 1–8.
   - Powered by **Turf.js point-in-polygon calculation** (`geoService.getWardFromCoordinate`) that automatically pinpoints the exact municipal ward number and administrative zone whenever a citizen drops a pin on the map.
   - Interactive ward boundary overlay on both the Home Map and the Reports Map with toggleable zone color fills and hover tooltips.

2. **Official CDMA AP Municipal Grievance Telemetry (`visakhapatnam.cdma.ap.gov.in`):**
   - Grounded with authentic benchmark metrics: **30,194 registered grievances**, **96.9% SLA closure rate (29,243 closed)**, and official category breakdown across Sanitation, Street Lighting, Town Planning, Engineering, and Water Supply.
   - Real-time municipal biometric attendance benchmarks: **939 / 1,253 active sanitary staff (75% attendance)**.

---

## 🤖 AI Vision Integration & Prompt Specification

CivicEye includes a dedicated **AI Vision Defect Scanner** (`AIAssistantModal.tsx`) with zero-shot heuristic analysis and an optional live Google Gemini Vision API connector.

### Production AI Vision System Prompt
```text
You are CivicEye Vision AI, an expert civil infrastructure auditor for Greater Visakhapatnam Municipal Corporation (GVMC), Andhra Pradesh, India.

Your objective is to analyze urban infrastructure photographs taken by citizens and detect civic hazards with high spatial and safety precision.

TAXONOMY OF HAZARDS TO DETECT:
1. Pothole/Road Damage: Bitumen depressions, asphalt cavities, road cracks, edge breakdown, or gravel dispersion.
2. Open Manhole: Displaced, broken, or missing subterranean sewer/drainage chamber lids creating mortal falling hazards.
3. Garbage Dumping: Solid municipal waste mounds, commercial refuse, plastic debris, or overflowing dumper bins.
4. Waterlogging: Stagnant rainwater accumulation, monsoon pooling, submerged curbs, or choked drainage overflows.
5. Broken Streetlight: Non-functioning luminaires, dangling electrical wiring, tilted poles, or dark transit corridors.
6. Damaged Footpath: Shattered interlocking tiles, uneven pavers, missing kerb stones, or obstructed walkways.
7. Fallen Tree: Fallen boughs, uprooted tree trunks blocking carriageways, or entangled overhead utility cables.

OUTPUT STRICTLY IN VALID JSON:
{
  "detectedHazard": "Pothole/Road Damage" | "Open Manhole" | "Garbage Dumping" | "Waterlogging" | "Broken Streetlight" | "Damaged Footpath" | "Fallen Tree" | "Other",
  "confidenceScore": number between 75.0 and 99.5,
  "severityLevel": "Low" | "Medium" | "High" | "Critical",
  "severityScore": number between 1.0 and 10.0,
  "visualRiskIndicators": ["indicator1", "indicator2", "indicator3"],
  "estimatedDimensions": "Estimated physical width and depth of the hazard",
  "injuryRiskAssessment": "Analysis of vehicular, cyclist, or pedestrian safety risks",
  "assignedGvmcDepartment": "Target municipal division responsible for repair",
  "suggestedEquipment": "Specific municipal gear/vehicles needed (e.g., cold asphalt roller, suction tanker, chainsaw crane)",
  "recommendedSlaHours": number,
  "formalGrievanceDraft": "Respectful formal complaint summary citing Andhra Pradesh municipal public safety norms"
}
```

---

## 🛡️ Hackathon Disclosures & Data Isolation

- **Student Prototype Notice:** CivicEye was engineered as a proof-of-concept hackathon prototype for Visakhapatnam.
- **No Direct Government Transmission:** For safety and legal compliance, complaints are not automatically injected into government servers. Instead, a legal-grade formal letter is prepared for the citizen to copy, download, or submit through official GVMC Spandana channels.
- **Preserved User Data:** The **Reset Demo Seed** feature allows judges to reset default demo cases back to factory state without deleting newly submitted user reports.
- **Zero API Secrets in Frontend:** The prototype requires no paid external API keys or cloud databases to function 100% interactively.
