import time # For creating delays in the countdown

def countdown_time(seconds):
    """Counts down from the specified time zero"""
    try:
        while seconds >= 0:
            m, s = divmod(seconds, 60)
            timer_display = f"{m:02d}:{s:02d}"
            print(timer_display, end='\r')  # Overwrites previous line
            time.sleep(1)
            seconds -= 1
    except KeyboardInterrupt:
        print("\n Countdown Interrupted!")
        
def get_user_time():
    """Prompts user to enter time in minutes or seconds"""
    while True:
        try:
            user_input = input("Please enter a time in minutes (i.e. '2m') or seconds (i.e. 60s): ").strip().lower()
            if user_input.endswith('m'):
                print("Time in minutes provided")
                return int(user_input[:-1]) * 60
            elif user_input.endswith('s'):
                return int(user_input[:-1])
            else:
                print("⚠️ Invalid format! Use 'Xm' for minutes or 'Ys' for seconds.")
        except ValueError:
            print("Invalid input!")

def alert_user():
    """Alerts the user when the timer ends"""
    print("\n⏰ Time's up! ⏰")
    try:
        # Works on most systems
        for _ in range(3):
            print("\a", end='')  # Terminal beep sound
            time.sleep(0.5)
    except:
        pass  # Ignore errors if sound doesn't play
    
if __name__ == "__main__":
    print("===== ⏳ Countdown Timer ⏳ =====")
    user_seconds = get_user_time()
    countdown_time(user_seconds)
    alert_user()
