from flask import Flask, render_template
import random

app = Flask(__name__)

# Lists for generating superhero attributes
ADJECTIVES = ["Super", "Mega", "Ultra", "Fantastic", "Cosmic", "Mighty", "Wonder", "Amazing", "Incredible", "Spectacular"]
NOUNS = ["Man", "Woman", "Boy", "Girl", "They", "Them", "Hero", "Savior", "Guardian", "Protector", "Defender", "Champion", "Warrior", "Knight", "Sentinel"]

# List of background stories
BACKGROUNDS = [
    "Bitten by a radioactive animal, they gained extraordinary powers.",
    "A scientific experiment gone wrong gave them unexpected abilities.",
    "Born with mutant genes, their powers manifested during puberty.",
    "Survived a catastrophic accident, emerging with superhuman abilities.",
    "Inherited powers from a mysterious family legacy.",
    "Gained abilities after exposure to a rare cosmic event.",
    "Touched by an ancient artifact, bestowing them with supernatural powers.",
    "Transformed by an alien technology during an invasion.",
    "Became a host to a powerful symbiote, granting them enhanced abilities.",
    "Developed superpowers after an exposure to a chemical spill.",
    "Trained in mystical arts by a secretive order, unlocking hidden powers.",
    "Fused with a mythical creature, gaining extraordinary abilities.",
    "Acquired powers through a wish granted by a supernatural being.",
    "Awakened latent abilities after a near-death experience.",
    "Survived an experiment with experimental serum, emerging as a hero.",
    "Discovered powers after coming into contact with a mysterious meteorite.",
    "Received powers through a pact with a powerful spirit or deity.",
    "Gained superhuman abilities after being struck by a magical lightning bolt.",
    "Enhanced by advanced cybernetic implants during a covert operation.",
    "Reborn with powers following a dramatic resurrection.",
    "Gained extraordinary abilities from an ancient prophecy.",
    "Exposed to a supercharged energy source, developing unique powers.",
    "Inherited abilities from an ancient warrior’s spirit.",
    "Accidentally merged with alien technology, acquiring advanced skills.",
    "Developed powers through an intensive and rigorous training regimen.",
    "Discovered hidden abilities through an ancient ritual or ceremony.",
    "Empowered by a cosmic entity during an otherworldly encounter.",
    "Survived a dimension-altering event, gaining new powers.",
    "Bitten by a genetically modified animal with unique traits.",
    "Enhanced by exposure to an experimental energy field.",
    "Accidentally transformed by a mysterious potion.",
    "Became a hero after surviving a cataclysmic event with altered genes.",
    "Gained powers through a fusion with another dimension’s energy.",
    "Gained abilities after being chosen by an ancient order of heroes.",
    "Received superpowers from a powerful ancient relic.",
    "Gained abilities from an unexpected exposure to a superpowerful artifact.",
    "Transformed by a secretive magical experiment.",
    "Fused with an interdimensional entity, granting them incredible abilities.",
    "Gained powers through a divine blessing during a sacred ritual.",
    "Enhanced through a highly advanced nanotechnology experiment.",
    "Acquired extraordinary powers after absorbing alien technology.",
    "Developed abilities through a rare and mystical cosmic phenomenon.",
    "Enhanced by an ancient elixir found in hidden ruins.",
    "Received extraordinary abilities through a cosmic blessing.",
    "Accidentally created a new form of energy within themselves, granting powers.",
    "Transformed by an enchanted item that bestowed them with incredible skills.",
    "Gained powers after being subjected to a series of mystical trials.",
    "Developed superpowers through a fusion with a powerful energy source.",
    "Gained abilities after receiving a divine artifact from a celestial being.",
    "Enhanced by exposure to an ancient magical storm.",
    "Accidentally merged with an otherworldly substance during an experiment.",
    "Gained extraordinary abilities after surviving a mythical curse.",
    "Developed powers through an ancient prophecy and subsequent trials.",
    "Transformed by a cosmic entity's intervention during a pivotal event.",
    "Received supernatural powers after a life-changing encounter with a deity."
]

HEIGHTS = [f"{feet}'{inches}" for feet in range(5, 8) for inches in range(12)]
WEIGHTS = [f"{weight} lbs" for weight in range(100, 301, 5)]
SKIN_COLORS = ["Fair", "Pale", "Light", "Medium", "Tan", "Dark", "Brown", "Black", "Olive", "Golden"]

# List of superhero powers
POWERS = [
    "Super Strength", "Flight", "Invisibility", "Telekinesis", "Mind Reading",
    "Teleportation", "Energy Projection", "Shapeshifting", "Healing Factor",
    "Time Manipulation", "Elemental Control", "Technopathy", "Gravity Manipulation", "Force Field Generation", "Sonic Scream", "X-Ray Vision",
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
WEAKNESSES = [
    "Kryptonite", "Fire", "Cold", "Water", "Electricity", "Sonic Waves", "Magic",
    "Sunlight", "Darkness", "Emotional Instability", "Limited Power Duration",
    "Physical Exhaustion", "Mental Fatigue", "Specific Material", "Energy Depletion", "Time Limit", "Power Nullification", "Extreme Heat",
    "Extreme Cold", "Poison", "Radiation", "Oxygen Deprivation", "Sensory Overload", "Phobias",
    "Family/Loved Ones", "Morality", "Pride", "Addiction", "Memory Loss", "Power Instability",
    "Uncontrollable Transformations", "Ancestral Curse", "Dimensional Interference", "Psychic Attacks",
    "Technological Dependency", "Biological Virus", "Soul Fragility", "Time Paradoxes", "Reality Warps",
    "Truth Serum", "Guilt", "Past Trauma", "Specific Sound Frequency", "Electromagnetic Pulses",
    "Nanite Infection", "Quantum Instability", "Parallel Universe Overlap", "Cosmic Radiation",
    "Interdimensional Energy", "Mythical Artifacts"
]

# List of personality traits
PERSONALITY_TRAITS = [
    "Courageous", "Compassionate", "Determined", "Intelligent", "Witty", "Stoic",
    "Energetic", "Calm", "Charismatic", "Humble", "Confident", "Loyal", "Analytical","Creative", "Patient",
    "Impulsive", "Cautious", "Optimistic", "Pessimistic", "Honest", "Secretive", "Sarcastic",
    "Gentle", "Fierce", "Adaptable", "Stubborn", "Curious", "Disciplined", "Emotional", "Logical",
    "Introverted", "Extroverted", "Perfectionist", "Laid-back", "Ambitious", "Modest", "Flamboyant",
    "Reserved", "Empathetic", "Competitive", "Cooperative", "Intuitive", "Methodical", "Passionate",
    "Aloof", "Quirky", "Serious", "Playful", "Responsible", "Free-spirited"
]

@app.route('/')
def generate_superhero():
    height = random.choice(HEIGHTS)
    weight = random.choice(WEIGHTS)
    skin_color = random.choice(SKIN_COLORS)

    hero_powers = random.sample(POWERS, k=random.randint(1, 3))
    weakness = random.choice(WEAKNESSES)
    traits = random.sample(PERSONALITY_TRAITS, k=random.randint(2, 4))

    power_adj = random.choice(hero_powers).split()[-1]
    first_name = random.choice([power_adj] + ADJECTIVES)
    last_name = random.choice(NOUNS)
    hero_name = f"{first_name} {last_name}"

    background = random.choice(BACKGROUNDS)

    return render_template(
        'superhero.html',
        hero_name=hero_name,
        background=background,
        height=height,
        weight=weight,
        skin_color=skin_color,
        powers=hero_powers,
        weakness=weakness,
        traits=traits
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')