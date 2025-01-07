// SRS (Spaced Repetition System) functionality
class SRSManager {
    constructor() {
        this.currentCard = null;
        this.reviewQueue = [];
        this.progress = JSON.parse(localStorage.getItem('characterProgress')) || {};
    }

    getDueCards() {
        const now = new Date();
        const dueCards = [];
        
        for (const [charId, data] of Object.entries(this.progress)) {
            if (new Date(data.nextReview) <= now) {
                dueCards.push(parseInt(charId));
            }
        }
        return dueCards;
    }

    updateProgress(characterId, correct) {
        const charData = this.progress[characterId] || {
            level: 0,
            reviews: 0,
            correctReviews: 0,
            nextReview: new Date().toISOString()
        };

        charData.reviews++;
        if (correct) {
            charData.level++;
            charData.correctReviews++;
            // Exponential spacing: 1, 2, 4, 8, 16 days...
            const interval = Math.pow(2, charData.level);
            charData.nextReview = new Date(Date.now() + interval * 24 * 60 * 60 * 1000).toISOString();
        } else {
            charData.level = Math.max(0, charData.level - 1);
            // Review again in 1 day if incorrect
            charData.nextReview = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
        }

        this.progress[characterId] = charData;
        localStorage.setItem('characterProgress', JSON.stringify(this.progress));

        // Update user progress
        const userProgress = JSON.parse(localStorage.getItem('userProgress'));
        userProgress.reviewHistory.push({
            date: new Date().toISOString(),
            characterId,
            correct
        });
        localStorage.setItem('userProgress', JSON.stringify(userProgress));
    }

    showNext() {
        if (this.reviewQueue.length === 0) {
            document.querySelector('.study-container').innerHTML = `
                <div class="text-center">
                    <h2>Review Complete!</h2>
                    <p>Great job! You've completed all reviews for now.</p>
                    <a href="/dashboard" class="btn btn-primary">Return to Dashboard</a>
                </div>
            `;
            return;
        }

        this.currentCard = this.reviewQueue.shift();
        this.updateUI();
    }

    updateUI() {
        const cardContainer = document.querySelector('.character-display');
        if (!cardContainer || !this.currentCard) return;

        cardContainer.innerHTML = `
            <div class="character-card p-4 mb-4">
                <div class="hanzi text-center mb-3">${this.currentCard.hanzi}</div>
                <div class="pinyin text-center mb-2">${this.currentCard.pinyin}</div>
                <div class="meaning text-center">${this.currentCard.meaning}</div>
            </div>
        `;
    }

    handleResponse(correct) {
        if (!this.currentCard) return;
        
        this.updateProgress(this.currentCard.id, correct);
        updateStreak();
        this.showNext();
    }
}

// Initialize SRS manager when study page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.study-container')) {
        window.srsManager = new SRSManager();
        
        // Initialize review queue from server-provided data
        const characters = JSON.parse(document.getElementById('study-data').textContent);
        window.srsManager.reviewQueue = characters;
        window.srsManager.showNext();
    }
});
