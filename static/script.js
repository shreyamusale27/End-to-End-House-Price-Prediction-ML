document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const priceResult = document.getElementById('price-result');
    const errorMsg = document.getElementById('error-msg');
    const spinner = document.getElementById('spinner');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI updates during fetch
        spinner.style.display = 'block';
        resultContainer.classList.add('hidden');
        errorMsg.textContent = '';
        priceResult.textContent = '--';
        
        // Gather data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Something went wrong');
            }
            
            // Format currency
            const formatter = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                maximumFractionDigits: 0
            });
            
            priceResult.textContent = formatter.format(result.price);
            
            // Adjust styling for success
            resultContainer.style.background = 'rgba(16, 185, 129, 0.1)';
            resultContainer.style.borderColor = 'rgba(16, 185, 129, 0.3)';
            priceResult.style.color = 'var(--success)';
            
        } catch (error) {
            errorMsg.textContent = error.message;
            
            // Adjust styling for error
            resultContainer.style.background = 'rgba(244, 63, 94, 0.1)';
            resultContainer.style.borderColor = 'rgba(244, 63, 94, 0.3)';
            priceResult.style.color = 'transparent';
        } finally {
            spinner.style.display = 'none';
            resultContainer.classList.remove('hidden');
            
            // Smooth scroll to result
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });

    // Auto-fill form with dummy data for rapid testing
    const fillDummyData = () => {
        const dummyData = {
            medinc: 8.32,
            houseage: 41,
            averooms: 6.98,
            avebedrms: 1.02,
            population: 322,
            aveoccup: 2.55,
            latitude: 37.88,
            longitude: -122.23
        };
        
        for (const [key, value] of Object.entries(dummyData)) {
            const el = document.getElementById(key);
            if (el && !el.value) {
                el.value = value;
            }
        }
    }
    
    // Fill the inputs right away if they are empty
    fillDummyData();
});
