import streamlit as st
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="My Daily Routine Tracker", page_icon="📊")

# App title
st.title("📊 My Daily Routine Tracker")

# Instructions
st.write("Enter the number of hours spent on each activity below.")
st.write("Total should be close to 24 hours.")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    studying = st.number_input("Studying (hours)", min_value=0.0, max_value=24.0, value=4.0, step=0.5)
    sleeping = st.number_input("Sleeping (hours)", min_value=0.0, max_value=24.0, value=8.0, step=0.5)

with col2:
    exercising = st.number_input("Exercising (hours)", min_value=0.0, max_value=24.0, value=1.0, step=0.5)
    social_media = st.number_input("Using Social Media (hours)", min_value=0.0, max_value=24.0, value=3.0, step=0.5)

# Calculate total hours
total_hours = studying + sleeping + exercising + social_media
other_hours = 24 - total_hours

# Display total hours
st.subheader(f"Total Hours: {total_hours:.1f} / 24")

# Color coding for total hours
if abs(total_hours - 24) <= 2:
    st.success("✅ Your total hours are close to 24 hours!")
elif total_hours > 24:
    st.error(f"⚠️ You've entered {total_hours:.1f} hours, which exceeds 24 hours!")
else:
    st.warning(f"ℹ️ You have {24-total_hours:.1f} unaccounted hours in your day.")

# Create data for pie chart
labels = ['Studying', 'Sleeping', 'Exercising', 'Social Media', 'Other']
sizes = [studying, sleeping, exercising, social_media, max(0, other_hours)]
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

# Remove 'Other' category if it's 0
if other_hours <= 0:
    labels = labels[:-1]
    sizes = sizes[:-1]
    colors = colors[:-1]

# Create pie chart
if total_hours > 0 or other_hours > 0:
    st.subheader("Daily Activity Distribution")
    
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%',
        startangle=90
    )
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Add a circle at the center to make it a donut chart (optional)
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Add title inside the donut hole
    ax.text(0, 0, 'Daily\nBreakdown', ha='center', va='center', fontsize=12)
    
    st.pyplot(fig)

# Display personalized messages
st.subheader("📋 Personalized Feedback")

if studying >= 6:
    st.success("🎓 **Great job!** You're dedicating good time to studying. Keep it up!")
elif studying >= 3:
    st.info("📚 Your study time is decent. Consider increasing it if you have academic goals.")
else:
    st.warning("📖 Consider allocating more time to studying for better academic performance.")

if social_media >= 5:
    st.error("📱 **Try to reduce your screen time.** High social media usage can affect productivity and sleep.")
elif social_media >= 3:
    st.warning("📱 Your social media usage is moderate. Be mindful of your screen time.")
else:
    st.success("👍 Good job keeping social media usage in check!")

if sleeping >= 7 and sleeping <= 9:
    st.success("😴 **Excellent!** You're getting the recommended amount of sleep.")
elif sleeping < 7:
    st.warning("💤 Consider getting more sleep. Adults typically need 7-9 hours for optimal health.")
else:
    st.info("💤 You're getting plenty of sleep. Make sure it's quality sleep!")

if exercising >= 0.5:
    st.success("🏃 **Well done!** You're making time for physical activity.")
else:
    st.info("💪 Try to incorporate some exercise into your daily routine for better health.")

# Add a reset button
if st.button("Reset All Values"):
    st.rerun()

# Add some helpful tips
with st.expander("💡 Tips for Better Time Management"):
    st.write("""
    1. **Plan your day** - Create a schedule the night before
    2. **Use time blocks** - Dedicate specific times for specific activities
    3. **Take breaks** - Use techniques like Pomodoro (25 min work, 5 min break)
    4. **Limit distractions** - Turn off notifications during focus time
    5. **Track your time** - Use apps to understand where your time goes
    6. **Set priorities** - Focus on important tasks first
    """)

# Footer
st.markdown("---")
st.caption("Track your daily routine to build better habits! ⏰")