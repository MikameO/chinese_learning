// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // Set initial theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);

    // Initialize user progress if not exists
    if (!localStorage.getItem('userProgress')) {
        localStorage.setItem('userProgress', JSON.stringify({
            charactersLearned: 0,
            streakDays: 0,
            lastStudyDate: null,
            reviewHistory: []
        }));
    }

    // Initialize character progress if not exists
    if (!localStorage.getItem('characterProgress')) {
        localStorage.setItem('characterProgress', JSON.stringify({}));
    }
});

// Character search functionality
const searchCharacter = (input) => {
    const characterCards = document.querySelectorAll('.character-card');
    const searchTerm = input.toLowerCase();

    characterCards.forEach(card => {
        const hanzi = card.querySelector('.hanzi').textContent;
        const pinyin = card.querySelector('.pinyin').textContent.toLowerCase();
        const meaning = card.querySelector('.meaning').textContent.toLowerCase();

        if (hanzi.includes(searchTerm) || 
            pinyin.includes(searchTerm) || 
            meaning.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
};

// Update streak
function updateStreak() {
    const progress = JSON.parse(localStorage.getItem('userProgress'));
    const today = new Date().toLocaleDateString();
    
    if (progress.lastStudyDate !== today) {
        if (new Date(progress.lastStudyDate) >= new Date(new Date().setDate(new Date().getDate() - 1))) {
            progress.streakDays++;
        } else {
            progress.streakDays = 1;
        }
        progress.lastStudyDate = today;
        localStorage.setItem('userProgress', JSON.stringify(progress));
    }
}

// Initialize learning session
function initializeLearning() {
    localStorage.setItem('userProgress', JSON.stringify({
        charactersLearned: 0,
        streakDays: 0,
        lastStudyDate: new Date().toLocaleDateString(),
        reviewHistory: []
    }));
    window.location.href = '/dashboard';
}
