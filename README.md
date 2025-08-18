Got it ✅
Here’s your **complete `README.md` file** — all sections merged into a single clean Markdown format ready for GitHub or submission.

````markdown
# Namma Uzhavan Nanban (நம்ம உழவன் நண்பன்) - Our Farmer's Friend

**A Hybrid AI Assistant for Paddy Farmers in Tamil Nadu**

**Video Demo Link:** [INSERT YOUR YOUTUBE/LOOM VIDEO LINK HERE]

---

## 🌾 The Problem

In Tamil Nadu, paddy farming is the backbone of our agriculture. However, farmers in remote areas often face a critical challenge: limited or no internet access. This **digital divide** cuts them off from vital, time-sensitive information they need to protect their crops and get a fair price for their harvest, leading to significant financial losses.

---

## 💡 Our Solution

**Namma Uzhavan Nanban** is an intelligent, bilingual AI assistant designed to solve this problem. It operates in a **hybrid online/offline mode**, ensuring farmers have a reliable tool in their hands—whether in the field or at home.  

The app’s core principle is **resilience**: it provides essential services offline and enhances capabilities when connected online.

---

## ✨ Key Features

- **Hybrid AI System:** Switches seamlessly between Google Gemini (online) and Ollama Phi-3 (offline).  
- **Fully Offline Disease Diagnosis:** Uses a custom-trained **PyTorch model** to identify 10 paddy diseases from leaf images and suggests remedies offline.  
- **Automated Daily Price Updates:**  
  1. Downloads latest market prices (PDF).  
  2. Converts & ingests into a searchable `market_price_db`.  
- **Dual-Database RAG:** Answers queries using both the price database and `rice_knowledge_base`.  
- **Live Weather Integration:** Fetches real-time weather data.  

---

## 🚧 Limitations & Future Work

- **Scope:** Currently focused only on **paddy farmers in Tamil Nadu**.  
- **Data Availability:** Built on limited public PDFs. Future work: collaborate with agricultural institutions for verified, larger datasets.  

---

## 🛠️ Technical Architecture

- **Backend:** Python, FastAPI  
- **Frontend:** HTML, CSS, JavaScript  
- **Online LLM:** Google Gemini 1.5 Flash  
- **Offline LLM:** Ollama with `phi3`  
- **Disease Model:** Custom-trained PyTorch (`.pt`)  
- **Databases:** ChromaDB (knowledge base + price DB)  
- **Scraper:** Python + Selenium  

---

## ⚙️ Installation & Setup

### **1. Prerequisites**

- Python **3.10+**  
- Google Chrome (for price data scraping)  
- [Ollama Desktop](https://ollama.com/) (offline AI runtime)  

---

### **2. Install Ollama**

1. Download & install from [ollama.com](https://ollama.com/)  
2. Verify installation:  
   ```bash
   ollama --version
````

---

### **3. Set Up Local AI Model**

```bash
ollama pull phi3
```

---

### **4. Clone Repository & Install Dependencies**

```bash
# Clone repo
git clone [YOUR_REPOSITORY_URL]
cd [PROJECT_FOLDER_NAME]

# Virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### **5. Configure API Keys**

Create a `.env` file in project root:

```ini
GOOGLE_API_KEY="your_google_api_key_here"
```

---

### **6. Build Knowledge Base**

```bash
python src/scripts/ingest.py
```

> Run once only. Price DB updates automatically each startup.

---

### **7. Run Application**

```bash
uvicorn main:app --reload
```

Open: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Testing Features

### **1. Offline Mode 🔴**

* **Action:** Disconnect internet (status turns red).

**Text Query:**

* Ask: *How do you manage bacterial leaf blight?*
  *(Tamil: பாக்டீரியா இலை கருகல் நோயை எவ்வாறு கட்டுப்படுத்துவது?)*
* **Expected:** Remedy from **phi3** model.

**Image Diagnosis:**

* Upload diseased paddy leaf.
* **Expected:** PyTorch predicts disease + phi3 suggests remedy.

---

### **2. Online Mode 🟢**

* **Action:** Reconnect internet (status turns green).

**Price Query:**

* Ask: *What is the price of BPT rice in Salem today?*
  *(Tamil: சேலத்தில் இன்று பிபிடி அரிசியின் விலை என்ன?)*
* **Expected:** Latest price from `market_price_db`.

**Hybrid Image Diagnosis:**

* Upload diseased leaf.
* **Expected:** PyTorch predicts disease + Gemini writes detailed Tamil answer.

**Weather Query:**

* Ask: *What is the weather in Chennai?*
  *(Tamil: சென்னையில் வானிலை எப்படி உள்ளது?)*
* **Expected:** Live weather data fetched via API.

---

## 📌 Summary

✅ Works offline & online
✅ Helps paddy farmers diagnose diseases & get remedies
✅ Auto-updates daily market rice prices
✅ Bilingual: Tamil + English
✅ Integrated weather & query support

---

```

Do you want me to **make this README shorter** (like a polished GitHub README with badges, sections, and minimal hackathon notes) or **keep it full-length** as a detailed hackathon submission document?
```
