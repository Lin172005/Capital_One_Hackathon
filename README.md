


##  **Namma Uzhavan Nanban (நம்ம உழவன் நண்பன்) - Our Farmer's Friend**

**A Hybrid AI Assistant for Paddy Farmers in Tamil Nadu**

**Video Demo Link:** [https://youtu.be/3P00RMJ6oiA]**

---

## **🌾 The Problem**

In Tamil Nadu, paddy farming is the backbone of our agriculture. However, farmers in remote areas often face a critical challenge: limited or no internet access. This **digital divide** cuts them off from the vital, time-sensitive information they need to protect their crops and get a fair price for their harvest, which can lead to significant financial losses.

## **💡 Our Solution**

**Namma Uzhavan Nanban** is an intelligent, bilingual AI assistant designed to solve this problem. It operates in a **hybrid online/offline mode**, ensuring that farmers have a reliable tool in their hands, whether they are in the field or at home with a connection. The application's core principle is **resilience**, providing essential services even when completely offline and intelligently enhancing its capabilities when online.

---

## **✨ Key Features**

* **Hybrid AI System:** Seamlessly switches between powerful online models (Google Gemini) and a 100% local AI (Ollama Phi-3) based on internet connectivity.
* **Fully Offline Disease Diagnosis:** Uses a custom-trained **PyTorch model** to accurately identify 10 different paddy diseases from an image, providing a detailed remedy using the local AI—no internet required.
* **Automated Daily Price Updates:** Since no official API exists, we built an automated pipeline that runs on startup:
    1.  It downloads the latest market prices from a web source as a PDF.
    2.  It ingests this data into a dedicated, searchable `market_price_db`.
* **Dual-Database RAG System:** For online queries, the app intelligently routes questions. It pulls price data from the fresh `market_price_db` and general knowledge from the main `rice_knowledge_base` to provide comprehensive, synthesized answers.
* **Live Weather Integration:** Connects to a live weather API to provide current conditions and forecasts.

---

## **🚧 Limitations & Future Work**

Given the time constraints of a hackathon, we made the following strategic decisions:
* **Narrow Focus:** We concentrated exclusively on **paddy farmers in Tamil Nadu** to create a deep and relevant tool.
* **Data Availability:** Our knowledge base was built from a limited set of publicly available agricultural PDFs. The next step is to collaborate with agricultural institutions to ingest more comprehensive and verified data.

---

## 🛠️ Technical Architecture

* **Backend:** Python, FastAPI
* **Frontend:** HTML, CSS, JavaScript
* **Online LLM:** Google Gemini 1.5 Flash
* **Offline LLM:** Ollama with `phi3`
* **Disease Model:** Custom-trained PyTorch model (`.pt`)
* **Vector Databases:** ChromaDB (for both the main KB and the daily price DB)
* **Automated Scraper:** Python with Selenium

---

## ⚙️ How to Install and Run

Please follow these steps carefully to set up and run the project.

### **1. Prerequisites**

* **Python 3.10+**
* **Google Chrome:** Required for the automated data pipeline.
* **Ollama Desktop:** The local AI server. See installation instructions below.

### **2. Install Ollama Desktop**

Ollama powers the application's offline capabilities. It must be installed and running in the background.

1.  **Download:** Go to the official website: [**ollama.com**](https://ollama.com/)
2.  **Install:** Download and run the installer for your operating system (Windows, macOS, or Linux). Follow the on-screen instructions.
3.  **Verify:** After installation, the Ollama application should be running. You can verify this by looking for the Ollama icon in your system tray or by opening a new terminal and running:
    ```bash
    ollama --version
    ```
    

### **3. Set Up the Local AI Model**

With Ollama running, open your terminal and pull the `phi3` model.
```bash
ollama pull phi3
````

### **4. Clone the Repository and Install Dependencies**

```bash
# Clone this project repository
git clone https://github.com/Lin172005/Capital_One_Hackathon.git
cd Capital_One_Hackathon

# Create and activate a Python virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install all required Python packages
pip install -r requirements.txt
```

### **5. Set Up Environment Variables**

1.  In the project's root folder, create a new file named `.env`.
2.  Add your Google Gemini API key to this file:
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    ```


***Note:** You only need to run this script once. The daily market price database is created and updated automatically every time the main application starts.*

### **6. Run the Application**

You are now ready to launch the server.
Run this first 
```bash
python main.py
```

```bash
uvicorn main:app --reload
```

The first time you run this command, it will automatically trigger the data pipeline. Once the startup process is complete, open your web browser and navigate to **`http://127.0.0.1:8000`**.

-----

## 🧪 How to Test the Features (Example Questions)

Follow this guide to test all core functionalities.

### **1. Test the OFFLINE Mode** 🔴

**Action:** **Disconnect your computer from the internet.** The status indicator in the app should turn red.

  * **Offline Text Query:**

      * Go to the "Query" tab.
      * **Ask:** `How do you manage bacterial leaf blight?` (or in Tamil: `பாக்டீரியா இலை கருகல் நோயை எவ்வாறு கட்டுப்படுத்துவது?`)
      * **Expected Result:** A detailed remedy from the local `phi3` model.

  * **Offline Image Diagnosis:**

      * Go to the "Image Diagnosis" tab.
      * **Action:** Upload an image of a diseased paddy leaf.
      * **Expected Result:** The app uses the local PyTorch model to identify the disease and `phi3` to generate a treatment plan.

### **2. Test the ONLINE Mode** 🟢

**Action:** **Reconnect your computer to the internet.** The status indicator should turn green.

  * **Online Price Query:**

      * Go to the "Query" tab.
      * **Ask:** `What is the price of BPT rice in Salem today?` (or in Tamil: `சேலத்தில் இன்று பிபிடி அரிசியின் விலை என்ன?`)
      * **Expected Result:** The app provides a current price from the auto-updated `market_price_db`.

  * **Online Hybrid Image Diagnosis:**

      * Go to the "Image Diagnosis" tab.
      * **Action:** Upload another diseased leaf image.
      * **Expected Result:** The app uses the **local PyTorch model** for the prediction and the **online Gemini model** to write a high-quality answer in Tamil.

  * **Live Weather Query:**

      * Go to the "Query" tab.
      * **Ask:** `What is the weather in Chennai?` (or in Tamil: `சென்னையில் வானிலை எப்படி உள்ளது?`)
      * **Expected Result:** The app will fetch and display live weather data.

<!-- end list -->

```
```



