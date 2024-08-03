from flask import Flask, render_template
import random

app = Flask(__name__)

# Lists for generating superhero names
adjectives = ["Super", "Mega", "Ultra", "Fantastic", "Cosmic", "Mighty", "Wonder", "Amazing", "Incredible", "Spectacular"]
nouns = ["Man", "Woman", "Boy", "Girl", "They", "Them", "Hero", "Savior", "Guardian", "Protector", "Defender", "Champion", "Warrior", "Knight", "Sentinel"]

# List of background stories
backgrounds = [
    "Bitten by a radioactive animal, they gained extraordinary powers.",
    "A scientific experiment gone wrong gave them unexpected abilities.",
    "Born with mutant genes, their powers manifested during puberty.",
    # ... (keep the rest of the backgrounds)
]

# New lists for physical attributes
heights = [f"{feet}'{inches}" for feet in range(5, 8) for inches in range(12)]
weights = [f"{weight} lbs" for weight in range(100, 301, 5)]
skin_colors = ["Fair", "Pale", "Light", "Medium", "Tan", "Dark", "Brown", "Black", "Olive", "Golden"]

# List of superhero powers
powers = [
    "Super Strength", "Flight", "Invisibility", "Telekinesis", "Mind Reading", "Teleportation",
    "Energy Projection", "Shapeshifting", "Healing Factor", "Time Manipulation", "Elemental Control",
    "Technopathy", "Gravity Manipulation", "Force Field Generation", "Sonic Scream", "X-Ray Vision",
    "Elasticity", "Phasing", "Duplication", "Animal Communication", "Size Alteration", "Magnetism Control",
    "Precognition", "Empathy", "Weather Control", "Energy Absorption", "Molecular Manipulation",
    "Adaptive Evolution", "Portal Creation", "Reality Warping", "Probability Manipulation",
    "Illusion Creation", "Power Mimicry", "Density Control", "Astral Projection", "Energy Constructs",
    "Dimensional Travel", "Superhuman Speed", "Superhuman Agility", "Superhuman Senses", "Wall-Crawling",
    "Underwater Breathing", "Poison Immunity", "Radiation Control", "Quantum Manipulation",
    "Psionic Blasts", "Dream Manipulation", "Memory Manipulation", "Superhuman Intelligence",
    "Light Manipulation", "Shadow Manipulation"
]

# List of weaknesses
weaknesses = [
    "Kryptonite", "Fire", "Cold", "Water", "Electricity", "Sonic Waves", "Magic", "Sunlight", "Darkness",
    "Emotional Instability", "Limited Power Duration", "Physical Exhaustion", "Mental Fatigue",
    "Specific Material", "Energy Depletion", "Time Limit", "Power Nullification", "Extreme Heat",
    "Extreme Cold", "Poison", "Radiation", "Oxygen Deprivation", "Sensory Overload", "Phobias",
    "Family/Loved Ones", "Morality", "Pride", "Addiction", "Memory Loss", "Power Instability",
    "Uncontrollable Transformations", "Ancestral Curse", "Dimensional Interference", "Psychic Attacks",
    "Technological Dependency", "Biological Virus", "Soul Fragility", "Time Paradoxes", "Reality Warps",
    "Truth Serum", "Guilt", "Past Trauma", "Specific Sound Frequency", "Electromagnetic Pulses",
    "Nanite Infection", "Quantum Instability", "Parallel Universe Overlap", "Cosmic Radiation",
    "Interdimensional Energy", "Mythical Artifacts"
]

# List of personality traits
personality_traits = [
    "Courageous", "Compassionate", "Determined", "Intelligent", "Witty", "Stoic", "Energetic",
    "Calm", "Charismatic", "Humble", "Confident", "Loyal", "Analytical", "Creative", "Patient",
    "Impulsive", "Cautious", "Optimistic", "Pessimistic", "Honest", "Secretive", "Sarcastic",
    "Gentle", "Fierce", "Adaptable", "Stubborn", "Curious", "Disciplined", "Emotional", "Logical",
    "Introverted", "Extroverted", "Perfectionist", "Laid-back", "Ambitious", "Modest", "Flamboyant",
    "Reserved", "Empathetic", "Competitive", "Cooperative", "Intuitive", "Methodical", "Passionate",
    "Aloof", "Quirky", "Serious", "Playful", "Responsible", "Free-spirited"
]

@app.route('/')
def generate_superhero():
    # Generate physical attributes
    height = random.choice(heights)
    weight = random.choice(weights)
    skin_color = random.choice(skin_colors)

    # Generate powers, weaknesses, and personality
    hero_powers = random.sample(powers, k=random.randint(1, 3))
    weakness = random.choice(weaknesses)
    traits = random.sample(personality_traits, k=random.randint(2, 4))

    # Generate name incorporating power
    power_adj = random.choice(hero_powers).split()[-1]
    first_name = random.choice([power_adj] + adjectives)
    last_name = random.choice(nouns)
    hero_name = f"{first_name} {last_name}"

    # Generate background
    background = random.choice(backgrounds)

    return render_template('superhero.html', 
                           hero_name=hero_name, 
                           background=background,
                           height=height,
                           weight=weight,
                           skin_color=skin_color,
                           powers=hero_powers,
                           weakness=weakness,
                           traits=traits)

if __name__ == '__main__':
    app.run(debug=True)