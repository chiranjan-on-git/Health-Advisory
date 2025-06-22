document.addEventListener('DOMContentLoaded', () => {
    // Existing elements
    const locationInput = document.getElementById('locationInput');
    const getAdvisoriesBtn = document.getElementById('getAdvisoriesBtn');
    const advisoriesOutput = document.getElementById('advisoriesOutput');
    const resultsArea = document.getElementById('resultsArea');
    const loadingIndicator = document.getElementById('loading');
    const errorArea = document.getElementById('errorArea');

    // Theme toggle elements
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const htmlElement = document.documentElement;
    const themeIcon = themeToggleBtn.querySelector('i'); // Get the icon element

    // --- Theme Switching Logic ---
    const THEME_KEY = 'themePreference';

    function applyTheme(theme) {
        if (theme === 'dark') {
            htmlElement.setAttribute('data-theme', 'dark');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        } else {
            htmlElement.removeAttribute('data-theme'); // Default is light
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    }

    function saveThemePreference(theme) {
        localStorage.setItem(THEME_KEY, theme);
    }

    function loadThemePreference() {
        const savedTheme = localStorage.getItem(THEME_KEY);
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme) {
            return savedTheme;
        } else if (prefersDarkScheme) {
            return 'dark';
        }
        return 'light'; // Default to light
    }

    // Initialize theme on page load
    const initialTheme = loadThemePreference();
    applyTheme(initialTheme);

    // Event listener for theme toggle button
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = htmlElement.hasAttribute('data-theme') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
        saveThemePreference(newTheme);
    });

    // Optional: Listen for OS theme changes (if no user preference is explicitly set)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (!localStorage.getItem(THEME_KEY)) {
            const newSystemTheme = event.matches ? 'dark' : 'light';
            applyTheme(newSystemTheme);
        }
    });
    // --- End Theme Switching Logic ---

    // Set a default example location
    locationInput.value = "California, United States";
    resultsArea.classList.add('hidden'); // Hide results area initially

    getAdvisoriesBtn.addEventListener('click', fetchAdvisories);
    locationInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            fetchAdvisories();
        }
    });

    async function fetchAdvisories() {
        const location = locationInput.value.trim();
        if (!location) {
            displayError("Please enter a location (e.g., State, Country).");
            return;
        }
        
        if (!location.includes(',')) {
            displayError("Please use the format 'State, Country'.");
            return;
        }

        loadingIndicator.classList.remove('hidden');
        resultsArea.classList.add('hidden');
        advisoriesOutput.textContent = '';
        errorArea.classList.add('hidden');

        try {
            const response = await fetch('http://localhost:5001/api/advisories', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ location: location }),
            });

            loadingIndicator.classList.add('hidden');

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: `HTTP error! Status: ${response.status}` }));
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            if (data.advisories) {
                advisoriesOutput.textContent = data.advisories;
                resultsArea.classList.remove('hidden');
            } else if (data.error) {
                displayError(data.error);
            } else {
                advisoriesOutput.textContent = `No relevant official medical advisories were found for ${location} in the last 30 days (or the API returned an empty result).`;
                resultsArea.classList.remove('hidden');
            }

        } catch (error) {
            loadingIndicator.classList.add('hidden');
            console.error('Error fetching advisories:', error);
            displayError(`Failed to fetch advisories: ${error.message}`);
        }
    }

    function displayError(message) {
        errorArea.textContent = message;
        errorArea.classList.remove('hidden');
        resultsArea.classList.add('hidden');
    }

    // Set current year in footer
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }
});