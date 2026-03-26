document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(100%)';
            msg.style.transition = 'all 0.5s ease';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });

    // Handle seat selection logic
    const seats = document.querySelectorAll('.seat.available');
    const totalPriceEl = document.getElementById('total-price');
    const seatInputEl = document.getElementById('selected-seats-input');
    const confirmBtn = document.getElementById('confirm-booking-btn');

    let selectedSeats = [];
    let totalPrice = 0;

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            const seatId = seat.dataset.id;
            const price = parseFloat(seat.dataset.price);

            if (seat.classList.contains('selected')) {
                // Deselect
                seat.classList.remove('selected');
                selectedSeats = selectedSeats.filter(id => id !== seatId);
                totalPrice -= price;
            } else {
                // Select
                seat.classList.add('selected');
                selectedSeats.push(seatId);
                totalPrice += price;
            }

            updateBookingInfo();
        });
    });

    function updateBookingInfo() {
        if (totalPriceEl) {
            totalPriceEl.textContent = `₹${totalPrice.toFixed(2)}`;
        }
        
        if (seatInputEl) {
            // Clear existing inputs
            seatInputEl.innerHTML = '';
            selectedSeats.forEach(id => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'seat_ids';
                input.value = id;
                seatInputEl.appendChild(input);
            });
        }
        
        if (confirmBtn) {
            if (selectedSeats.length > 0) {
                confirmBtn.removeAttribute('disabled');
                confirmBtn.classList.remove('ghost-btn');
                confirmBtn.classList.add('neon-btn-red');
            } else {
                confirmBtn.setAttribute('disabled', 'true');
                confirmBtn.classList.remove('neon-btn-red');
                confirmBtn.classList.add('ghost-btn');
            }
        }
    }
});
