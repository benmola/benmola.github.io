# Portfolio Automation and Redesign Walkthrough

This document outlines the changes made to your portfolio website to automate updates and enhance the visual design.

## 1. Automation Setup (GitHub Actions)

We have created a GitHub Actions workflow that automates the following:

*   **Trigger:** The workflow runs automatically whenever you push changes to the `Python/` directory, `CV.tex`, or `cv-data.json`. It also runs daily at midnight.
*   **Process:**
    1.  Checks out your repository.
    2.  Sets up Python and installs dependencies.
    3.  Installs LaTeX (for CV generation).
    4.  Runs the `auto_update.py` script to generate HTML pages and the PDF CV.
    5.  Commits and pushes the generated files back to your repository.

**File:** `.github/workflows/update_site.yml`

## 2. Visual Redesign

We have significantly improved the look and feel of your website:

*   **Modern Aesthetic:** Switched to a "Deep Teal & Slate" theme with glassmorphism effects and rounded corners.
*   **Dark Mode:** Implemented a toggleable Dark Mode that persists user preference.
*   **Typography:** Adopted "Montserrat" for headers and "Inter" for body text.
*   **Animations:** Added fade-in animations for cards and smooth scrolling for navigation.
*   **Interactive Elements:** Enhanced hover effects and added a dynamic sidebar.

## 3. Files Modified

*   `.github/workflows/update_site.yml`: The automation workflow.
*   `assets/styles.css`: The stylesheet containing the new design and Dark Mode variables.
*   `index.js`: New JavaScript file for Dark Mode logic and scroll animations.
*   `Python/generate_html.py`: Updated to link the new CSS, fonts, and JS file.

## 4. How to Use

1.  **Update Content:** Edit `cv-data.json` or `publications.html` (if you want to extract from there) to update your information.
2.  **Push Changes:** Commit and push your changes to GitHub.
    ```bash
    git add .
    git commit -m "Update portfolio content"
    git push origin main
    ```
3.  **Automatic Update:** The GitHub Action will trigger, generate the new HTML and PDF files, and update your live site.

## 5. Manual Trigger

You can also manually trigger the update from the "Actions" tab in your GitHub repository if needed.
