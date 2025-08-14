

# Capital One Launchpad: Tamil Nadu Agri-Expert 🚀

This project is our submission for the Capital One Launchpad hackathon. We are building a "Digital Smart Farmer" to help farmers in Tamil Nadu.

**Current MVP Goal:** The "Rice Lifeline" Agent. An AI assistant that helps a rice farmer identify a crop disease, suggests a low-cost treatment, and finds a micro-loan to finance it.

## 💻 Getting Started: Local Setup

Follow these steps to get the project running on your local machine.

### 1\. Clone the Repository

Open your terminal or command prompt and clone the project.

```bash
git clone https://github.com/Lin172005/Capital_One_Hackathon.git
cd Capital_One_Hackathon
```

### 2\. Create and Activate Virtual Environment

This keeps our project's dependencies isolated.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (you must do this every time you work on the project)
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3\. Install Dependencies

This command installs all the necessary Python packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Set Up Your Environment Variables

We need to provide the secret API key to the application.

1.  Create a new file in the main project folder named `.env`.

2.  Open the `.env` file and add the following line, replacing `YOUR_KEY_HERE` with the actual Google AI API key. (Ask the project lead for the key if you don't have it).

    ```
    GOOGLE_API_KEY="YOUR_KEY_HERE"
    ```

### 5\. Verify Your Setup

Run the prototype script to make sure everything is working correctly.

```bash
python src/scripts/rag_prototype.py
```

You should see output detailing the ingestion, retrieval, and final generated answer without any errors.

-----

## 🌿 Development Workflow: How to Contribute

To keep our `main` branch stable, all new work must be done on a separate branch.

### 1\. Get the Latest Code

Before starting any new work, always make sure your `main` branch is up-to-date.

```bash
git checkout main
git pull origin main
```

### 2\. Create a New Branch

Create a new branch for your feature or fix. Please follow our naming convention.

**Branch Naming Convention:**

  * For new features: `feature/<short-description>`
  * For bug fixes: `fix/<short-description>`

<!-- end list -->

```bash
# Example for a new feature
git checkout -b feature/process-pdf-data

# Example for a bug fix
git checkout -b fix/api-error-handling
```

### 3\. Make Your Changes

Work on your code in this new branch. Once you have made progress, commit your changes with a clear message.

```bash
# Stage your changes
git add .

# Commit them
git commit -m "feat: Add function to read text from PDFs"
```

### 4\. Push Your Branch to GitHub

Share your branch with the team by pushing it to the remote repository.

```bash
# Use the same branch name you created
git push origin feature/process-pdf-data
```

### 5\. Create a Pull Request (PR)

Go to the project's GitHub page. You will see a prompt to create a **Pull Request** from your new branch.

1.  Click the "Compare & pull request" button.
2.  Give your PR a clear title and a brief description of the changes.
3.  Assign another team member to review your code.
4.  Once reviewed and approved, the PR can be merged into the `main` branch.