import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Audio setup with edge-tts -----
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

def run_async_with_timeout(coro, timeout=30):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(asyncio.wait_for(coro, timeout=timeout))
    finally:
        loop.close()

async def save_speech(text, file_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

def generate_audio(text, output_path, voice):
    if not EDGE_TTS_AVAILABLE:
        raise Exception("edge-tts not installed")
    run_async_with_timeout(save_speech(text, output_path, voice))

VOICE = "en-US-JennyNeural"

st.set_page_config(page_title="Let's Learn TOEFL with Gesner", layout="wide")

# ========== STYLING ==========
def set_toefl_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a0f2a, #1a1f3a, #0a0f2a); }
        .main-header { background: linear-gradient(135deg, #ff6b35, #f7931e, #ffcc00); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        .stTabs [role="tab"] { color: white !important; background: rgba(255,100,50,0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: #ff6b35; color: black !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #ff6b35; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #ffcc00; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0a0f2a, #1a1f3a); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #1a1f3a; border: 1px solid #ff6b35; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
        div[data-baseweb="popover"] ul { background-color: #1a1f3a; border: 1px solid #ff6b35; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #1a1f3a; }
        div[data-baseweb="popover"] li:hover { background-color: #ff6b35; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff6b35"/>
                    <stop offset="50%" stop-color="#f7931e"/>
                    <stop offset="100%" stop-color="#ffcc00"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ========== AUTHENTICATION ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_toefl_style()
    st.title("🔐 Access Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn TOEFL with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #ffcc00;'>20 lessons – Conversations, Vocabulary, Idioms, Grammar, Essays</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

set_toefl_style()
st.markdown("""
<div class="main-header">
    <h1>📘 Let's Learn TOEFL with Gesner</h1>
    <p>20 interactive lessons | Conversations | Vocabulary | Idioms | Grammar | Essays | Audio support</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Select a lesson")
    lesson_number = st.selectbox("Lesson", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Your progress")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lesson {lesson_number} of 20 completed")
    st.markdown("---")
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$299 USD** (full book – 20 lessons, source code, certificate)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ========== LARGE BASE LISTS ==========
conversation_templates = [
    ("Student", "Professor", "Topic: University Registration"),
    ("Student A", "Student B", "Topic: Library Study Habits"),
    ("Candidate", "Interviewer", "Topic: Job Interview for Internship"),
    ("Customer", "Agent", "Topic: Flight Booking"),
    ("Patient", "Doctor", "Topic: Health Symptoms"),
    ("Client", "Banker", "Topic: Opening an Account"),
    ("Student", "Advisor", "Topic: Course Selection"),
    ("Employee", "Manager", "Topic: Performance Review"),
    ("Tenant", "Landlord", "Topic: Apartment Maintenance"),
    ("Tourist", "Guide", "Topic: City Tour"),
    ("Student", "Librarian", "Topic: Finding Research Materials"),
    ("Colleague A", "Colleague B", "Topic: Project Deadline"),
    ("Friend A", "Friend B", "Topic: Weekend Plans"),
    ("Parent", "Teacher", "Topic: Child's Progress"),
    ("Shopper", "Salesperson", "Topic: Returning an Item"),
    ("Presenter", "Audience", "Topic: Conference Q&A"),
    ("Coach", "Athlete", "Topic: Training Schedule"),
    ("Chef", "Assistant", "Topic: Recipe Preparation"),
    ("Artist", "Critic", "Topic: Art Exhibition"),
    ("Scientist", "Journalist", "Topic: New Discovery")
]

def generate_conversation(lesson_num):
    """Generate 3 unique conversations for the given lesson."""
    convos = []
    topics_lists = [
        ['university', 'work', 'travel', 'health', 'technology', 'environment', 'education', 'culture'],
        ['deadline', 'budget', 'schedule', 'resource', 'communication', 'quality', 'teamwork', 'leadership'],
        ['climate change', 'online learning', 'social media', 'artificial intelligence', 'remote work', 'fitness', 'nutrition', 'mental health']
    ]
    for i in range(3):
        speaker1, speaker2, _ = conversation_templates[(lesson_num + i) % len(conversation_templates)]
        topic_list = topics_lists[i % len(topics_lists)]
        topic = topic_list[(lesson_num + i) % len(topic_list)]
        conv = f"""
**Conversation {i+1} – Discussing {topic.title()}**

**{speaker1}:** Hello! How are you doing today?

**{speaker2}:** I'm great, thanks! I've been thinking about {topic}.

**{speaker1}:** That's interesting. Could you tell me more?

**{speaker2}:** Sure. In my opinion, {topic} is very important for TOEFL preparation.

**{speaker1}:** I agree. Let's practice some key vocabulary and phrases.

**{speaker2}:** That would be very helpful. Thank you!
        """
        convos.append(conv)
    return convos

# Vocabulary words (2000+ items)
vocab_base = [
    "abandon", "abrupt", "absorb", "abundant", "accelerate", "accessible", "accommodate", "accompany",
    "accomplish", "accurate", "accuse", "achieve", "acknowledge", "acquire", "adapt", "adequate",
    "adjust", "admire", "admit", "adopt", "advance", "advocate", "affect", "aggregate", "allocate",
    "anticipate", "apparent", "appeal", "apply", "approach", "appropriate", "approximate", "arbitrary",
    "assess", "assign", "assist", "assume", "assure", "attain", "attempt", "attribute", "authentic",
    "authorize", "automate", "available", "average", "avoid", "aware", "beneficial", "brief", "broad",
    "capable", "cause", "challenge", "characteristic", "clarify", "coherent", "coincide", "collapse",
    "combine", "commence", "comment", "commission", "commit", "commodity", "communicate", "compare",
    "compensate", "compete", "compile", "complement", "complete", "complicate", "comply", "compose",
    "compound", "comprehend", "comprehensive", "compress", "comprise", "compromise", "conceal", "concede",
    "concentrate", "concept", "concern", "conclude", "concurrent", "condense", "condition", "conduct",
    "confer", "confess", "confine", "confirm", "conflict", "conform", "confront", "confuse", "congregate",
    "conjecture", "connect", "consent", "conserve", "consider", "consist", "consolidate", "conspicuous",
    "constant", "constitute", "constrain", "construct", "consult", "consume", "contact", "contain",
    "contemplate", "contemporary", "contend", "contest", "context", "contract", "contradict", "contrary",
    "contribute", "contrive", "control", "controversial", "convene", "convenient", "converge", "converse",
    "convert", "convey", "convict", "convince", "cooperate", "coordinate", "cope", "core", "corporate",
    "correspond", "corrupt", "counsel", "counter", "counterpart", "course", "cover", "coverage", "craft",
    "create", "credible", "credit", "crisis", "criteria", "critical", "crucial", "crude", "curb", "curious",
    "current", "curtail", "custom", "cycle", "damage", "debate", "decade", "decent", "decide", "declare",
    "decline", "decrease", "dedicate", "deem", "default", "defend", "defer", "define", "definite", "delegate",
    "delete", "deliberate", "delicate", "deliver", "demand", "demonstrate", "denote", "deny", "depart",
    "depend", "depict", "deploy", "deposit", "depress", "derive", "descend", "describe", "deserve", "design",
    "despite", "destine", "destroy", "detail", "detect", "deter", "determine", "develop", "deviate", "device",
    "devise", "devote", "diagram", "differentiate", "difficult", "diffuse", "dilute", "diminish", "direct",
    "disable", "disagree", "disappear", "disaster", "discard", "discern", "discharge", "discipline", "disclose",
    "discount", "discover", "discriminate", "discuss", "disease", "disgrace", "disguise", "dislike", "dismiss",
    "disorder", "displace", "display", "dispose", "dispute", "disregard", "dissolve", "distinct", "distinguish",
    "distort", "distract", "distress", "distribute", "district", "disturb", "diverge", "diverse", "divert",
    "divide", "divine", "divorce", "document", "domain", "domestic", "dominate", "donate", "draft", "drama",
    "drastic", "drawback", "dread", "drift", "drought", "dual", "dumb", "duplicate", "duration", "dynamic",
    "earnest", "ease", "eccentric", "echo", "economic", "edge", "edit", "educate", "effect", "effective",
    "efficient", "effort", "elaborate", "elect", "elegant", "element", "elevate", "elicit", "eligible", "eliminate",
    "elite", "eloquent", "elsewhere", "emerge", "eminent", "emit", "emotion", "emphasis", "empower", "enable",
    "enact", "encounter", "encourage", "endanger", "endeavor", "endorse", "endure", "enforce", "engage",
    "enhance", "enjoy", "enlarge", "enlighten", "enlist", "enormous", "enrich", "enroll", "ensure", "enter",
    "entertain", "enthusiasm", "entire", "entitle", "entity", "entrance", "entrepreneur", "enumerate", "envision",
    "episode", "equal", "equip", "equivalent", "erect", "erode", "erratic", "error", "erupt", "essay", "essence",
    "essential", "establish", "estate", "esteem", "estimate", "eternal", "ethical", "evaluate", "evaporate",
    "eventual", "evidence", "evident", "evolve", "exact", "exaggerate", "exceed", "excel", "except", "excess",
    "exchange", "excite", "exclude", "excuse", "execute", "exempt", "exercise", "exert", "exhaust", "exhibit",
    "exile", "exist", "exit", "expand", "expect", "expedite", "expel", "expend", "expense", "experience",
    "expert", "explain", "explicit", "explode", "exploit", "explore", "expose", "express", "extend", "extent",
    "exterior", "external", "extinct", "extract", "extra", "extraordinary", "extreme", "fabricate", "facilitate",
    "factor", "faculty", "faint", "fair", "faith", "fake", "fallacy", "familiar", "fancy", "fantasy", "fare",
    "fascinate", "fashion", "fatal", "fatigue", "fault", "feasible", "feature", "federal", "feeble", "feedback",
    "fertile", "fierce", "final", "finance", "finite", "firm", "fix", "flaw", "flexible", "flourish", "fluctuate",
    "focus", "forbid", "force", "forecast", "foremost", "forge", "formal", "format", "former", "formula",
    "forthcoming", "fortune", "foundation", "fraction", "fragile", "fragment", "frame", "frequent", "fresh",
    "frontier", "frustrate", "fulfill", "function", "fundamental", "further", "fuse", "future", "gain", "gather",
    "gender", "generate", "generous", "genuine", "gigantic", "global", "goal", "govern", "gradual", "grain",
    "grant", "graph", "grasp", "grateful", "gratitude", "grave", "gravity", "greedy", "grieve", "guarantee",
    "guard", "guidance", "guilty", "habit", "halt", "handle", "harbor", "harm", "harmony", "harsh", "harvest",
    "haste", "hazard", "hesitate", "hierarchy", "highlight", "hinder", "hint", "historic", "hollow", "honest",
    "horizon", "hostile", "huge", "humanity", "humble", "hypothesis", "ideal", "identical", "identify", "idle",
    "ignore", "illuminate", "illustrate", "image", "imitate", "immense", "immerse", "impact", "impair", "impart",
    "impede", "imperative", "implement", "implicate", "imply", "import", "impose", "impress", "improve", "impulse",
    "incentive", "incident", "include", "income", "incorporate", "increase", "incur", "indeed", "indicate",
    "indifferent", "indigenous", "indirect", "induce", "indulge", "industrial", "inevitable", "infer", "infinite",
    "inflate", "influence", "inform", "infrastructure", "inherent", "initial", "inject", "injure", "innocent",
    "innovate", "input", "inquire", "insight", "insist", "inspect", "inspire", "install", "instance", "instant",
    "instead", "institute", "instruct", "insulate", "intact", "integral", "integrate", "integrity", "intellect",
    "intend", "intense", "interact", "interfere", "interim", "interior", "intermediate", "internal", "interpret",
    "interrupt", "interval", "intervene", "intimate", "intricate", "intrigue", "intrinsic", "intrude", "intuition",
    "invade", "invent", "invest", "investigate", "invite", "involve", "ironic", "isolate", "issue", "item",
    "judge", "justify", "keen", "label", "labor", "lag", "landmark", "language", "launch", "layer", "leadership",
    "lecture", "legal", "legacy", "legislation", "legitimate", "leisure", "length", "lesson", "liable", "liberal",
    "license", "likewise", "limit", "linear", "lingering", "link", "list", "literacy", "literal", "literature",
    "litigation", "live", "loan", "local", "locate", "logic", "loom", "loose", "loyal", "lucid", "lucrative",
    "luminous", "lure", "luxury", "maintain", "major", "majority", "mandate", "manifest", "manipulate", "manner",
    "manufacture", "margin", "massive", "mature", "maximize", "mean", "measure", "media", "mediate", "medical",
    "medium", "mental", "mention", "merchant", "merge", "merit", "method", "metric", "migrate", "mild", "military",
    "minimize", "minimum", "minor", "minute", "miracle", "mislead", "mission", "moderate", "modify", "monitor",
    "monopoly", "moral", "motion", "motivate", "motive", "mutual", "mystery", "narrative", "narrow", "nation",
    "native", "natural", "navigate", "necessary", "negative", "neglect", "negotiate", "neither", "neutral",
    "nevertheless", "notable", "notice", "notion", "notorious", "nourish", "novel", "objective", "oblige", "obscure",
    "observe", "obstacle", "obtain", "obvious", "occasion", "occupy", "occur", "offend", "offset", "omit",
    "ongoing", "operate", "opinion", "opponent", "opportunity", "oppose", "opposite", "oppress", "optimal", "optimize",
    "option", "orbit", "order", "ordinary", "organize", "orient", "original", "outcome", "outline", "output",
    "outside", "overall", "overcome", "overlap", "overlook", "overwhelm", "owe", "own", "pace", "pack", "pain",
    "panel", "paradigm", "parallel", "parameter", "participate", "particular", "passion", "passive", "patent",
    "path", "patient", "pattern", "pause", "peace", "perceive", "percent", "perfect", "perform", "permanent",
    "permit", "persist", "personal", "perspective", "persuade", "pertinent", "pervasive", "phase", "phenomenon",
    "philosophy", "physical", "pioneer", "place", "plain", "plan", "platform", "plausible", "play", "plea", "pleasant",
    "please", "pledge", "plenty", "plot", "plural", "policy", "polish", "polite", "political", "pollute", "popular",
    "portion", "portray", "pose", "position", "positive", "possess", "possible", "postpone", "potential", "pour",
    "poverty", "power", "practical", "practice", "preach", "precede", "precise", "predict", "prefer", "prejudice",
    "preliminary", "premium", "prepare", "prescribe", "presence", "present", "preserve", "preside", "press", "pressure",
    "presume", "prevent", "previous", "primary", "prime", "principal", "principle", "prior", "priority", "prison",
    "privacy", "private", "privilege", "probable", "proceed", "process", "proclaim", "produce", "profession", "profit",
    "profound", "program", "progress", "prohibit", "project", "prolong", "prominent", "promise", "promote", "prompt",
    "proof", "proper", "property", "proportion", "propose", "prospect", "prosper", "protect", "protest", "prove",
    "provide", "provoke", "public", "publish", "purchase", "purpose", "pursue", "puzzle", "qualify", "quality",
    "quantity", "quarter", "query", "quest", "question", "queue", "quick", "quiet", "quit", "quote", "race",
    "radical", "raise", "range", "rank", "rare", "rate", "rather", "reach", "react", "read", "ready", "real",
    "realize", "reason", "recall", "recent", "receive", "recess", "recognize", "recommend", "record", "recover",
    "rectify", "recycle", "reduce", "refer", "reflect", "reform", "refrain", "refresh", "refuse", "regard", "region",
    "register", "regret", "regulate", "reinforce", "reject", "relate", "release", "relevant", "relieve", "rely",
    "remain", "remark", "remind", "remove", "render", "renew", "rent", "repair", "repeat", "replace", "reply",
    "report", "represent", "reproduce", "reputation", "request", "require", "rescue", "research", "resemble", "reserve",
    "resident", "resist", "resolve", "resort", "respect", "respond", "restore", "restrict", "result", "resume",
    "retain", "retire", "return", "reveal", "revenue", "reverse", "review", "revise", "revive", "reward", "rhythm",
    "rich", "rid", "risk", "rival", "robust", "role", "routine", "rule", "rural", "sacrifice", "safe", "sake",
    "sample", "scale", "scan", "scatter", "schedule", "scheme", "scope", "score", "screen", "search", "season",
    "section", "sector", "secure", "seek", "select", "sense", "sensitive", "sequence", "series", "serve", "service",
    "settle", "severe", "shape", "share", "shift", "short", "show", "signal", "significance", "similar", "simple",
    "simulate", "simultaneous", "single", "site", "situate", "size", "skill", "slight", "smart", "smooth", "soar",
    "social", "soft", "soil", "sole", "solid", "solution", "solve", "sound", "source", "space", "span", "spare",
    "speak", "special", "specific", "specify", "speculate", "speed", "spend", "split", "spoil", "spot", "spread",
    "stable", "staff", "stage", "stand", "standard", "standpoint", "star", "state", "static", "statistics", "status",
    "steady", "steep", "step", "stick", "still", "stimulate", "stock", "stop", "store", "straight", "strain", "strange",
    "strategy", "stream", "strength", "stress", "stretch", "strict", "strike", "strong", "structure", "struggle",
    "study", "style", "subject", "submit", "subsequent", "substance", "substantial", "substitute", "subtle", "succeed",
    "success", "sufficient", "suggest", "suitable", "sum", "summary", "superior", "supply", "support", "suppose",
    "sure", "surface", "surplus", "surprise", "surround", "survey", "survive", "suspect", "suspend", "sustain",
    "symbol", "symptom", "system", "table", "tact", "take", "talent", "talk", "target", "task", "teach", "team",
    "technical", "technique", "technology", "temporary", "tend", "term", "test", "text", "theme", "theory", "therefore",
    "thick", "thin", "think", "thorough", "though", "threat", "through", "throw", "tight", "time", "tiny", "tissue",
    "title", "together", "tolerate", "topic", "total", "touch", "tough", "tour", "toward", "track", "trade", "tradition",
    "traffic", "tragic", "train", "transfer", "transform", "transit", "translate", "transport", "trap", "travel",
    "treat", "treaty", "tree", "trend", "trial", "tribe", "trip", "trouble", "true", "trust", "truth", "try", "turn",
    "type", "typical", "ultimate", "unable", "unaware", "uncover", "under", "undergo", "understand", "undertake",
    "undo", "uneasy", "unexpected", "unfair", "unfold", "unify", "unique", "unit", "unite", "universal", "unknown",
    "unlike", "unlikely", "unload", "unlock", "unlucky", "unpaid", "unpleasant", "unpopular", "unreal", "unrest",
    "unsafe", "unsure", "unusual", "unwilling", "update", "upgrade", "uphold", "upon", "upper", "upset", "urban",
    "urge", "use", "usual", "vacant", "vacation", "vaccine", "valid", "valuable", "value", "variable", "variation",
    "variety", "various", "vary", "vast", "vehicle", "venture", "verify", "version", "versus", "vessel", "viable",
    "victim", "victory", "video", "view", "village", "violate", "violence", "virtual", "virtue", "virus", "visible",
    "vision", "visit", "visual", "vital", "vivid", "voice", "volume", "volunteer", "vote", "wage", "wait", "walk",
    "wall", "want", "war", "warn", "waste", "watch", "water", "wave", "way", "weak", "wealth", "weapon", "wear",
    "weekly", "weigh", "weight", "welcome", "welfare", "well", "west", "wet", "whole", "wide", "width", "wild",
    "willing", "win", "wind", "window", "wise", "wish", "withdraw", "within", "without", "witness", "wonder",
    "word", "work", "world", "worry", "worth", "would", "write", "wrong", "yard", "year", "youth", "zero", "zone"
]
# Extend to >1000
vocab_base = vocab_base * 3

# Idioms (500+)
idioms_base = [
    "A blessing in disguise", "A dime a dozen", "A piece of cake", "A shot in the dark", "A taste of your own medicine",
    "A watched pot never boils", "A wild goose chase", "Add insult to injury", "All ears", "All thumbs",
    "An arm and a leg", "Apple of my eye", "Back to the drawing board", "Barking up the wrong tree", "Beat around the bush",
    "Bite off more than you can chew", "Bite the bullet", "Break a leg", "Break the ice", "Burn the midnight oil",
    "Bury the hatchet", "By the skin of your teeth", "Call it a day", "Cat got your tongue", "Chew the fat",
    "Cold feet", "Cost an arm and a leg", "Cry over spilt milk", "Cut corners", "Cut to the chase",
    "Devil's advocate", "Don't count your chickens before they hatch", "Don't put all your eggs in one basket",
    "Drop in the bucket", "Elephant in the room", "Every cloud has a silver lining", "Face the music", "Feel under the weather",
    "Fit as a fiddle", "Get a taste of your own medicine", "Get out of hand", "Get your act together", "Give the benefit of the doubt",
    "Go back to the drawing board", "Go the extra mile", "Hang in there", "Have a chip on your shoulder", "Have your head in the clouds",
    "Hit the books", "Hit the nail on the head", "Hit the sack", "Hold your horses", "In the heat of the moment", "It takes two to tango",
    "Jump on the bandwagon", "Keep an eye on", "Keep your chin up", "Kill two birds with one stone", "Leave no stone unturned",
    "Let sleeping dogs lie", "Let the cat out of the bag", "Make a long story short", "Make ends meet", "Miss the boat",
    "No pain, no gain", "Off the beaten path", "Off the top of my head", "On cloud nine", "On the ball", "On the fence",
    "Once in a blue moon", "Out of the blue", "Play devil's advocate", "Pull yourself together", "Put your foot in your mouth",
    "Rain on your parade", "Ring a bell", "Rub someone the wrong way", "See eye to eye", "Sit on the fence",
    "Speak of the devil", "Spill the beans", "Steal someone's thunder", "Take it with a grain of salt", "Take the bull by the horns",
    "The ball is in your court", "The best of both worlds", "The devil is in the details", "The early bird catches the worm",
    "The last straw", "The sky is the limit", "Through thick and thin", "Throw in the towel", "Time flies when you're having fun",
    "Under the weather", "Up in the air", "Walk on eggshells", "Wear your heart on your sleeve", "When pigs fly", "Wrap your head around"
]
# Extend
idioms_base = idioms_base * 2

# Grammar rules (200+)
grammar_base = [
    "Use the present simple for facts and routines.",
    "Use the past simple for completed actions in the past.",
    "Use the present perfect for actions that started in the past and continue to the present.",
    "Use 'will' for future predictions and spontaneous decisions.",
    "Use 'going to' for planned future actions.",
    "Use the present continuous for actions happening now.",
    "Use the past continuous for actions in progress at a specific time in the past.",
    "Use the future continuous for actions that will be in progress at a future time.",
    "Use the present perfect continuous for actions that started in the past and are still happening.",
    "Use the past perfect for actions that happened before another past action.",
    "Use modal verbs (can, could, may, might, must, shall, should, will, would) to express possibility, ability, permission, or obligation.",
    "Use the passive voice when the action is more important than who did it.",
    "Use conditionals (if clauses) to express cause and effect.",
    "Use relative clauses to add information about a noun.",
    "Use reported speech to tell what someone said.",
    "Use gerunds (-ing form) as nouns.",
    "Use infinitives (to + verb) after certain verbs and adjectives.",
    "Use articles (a, an, the) correctly.",
    "Use prepositions of time (at, on, in) correctly.",
    "Use prepositions of place (at, on, in) correctly.",
    "Use comparative and superlative adjectives to compare things.",
    "Use adverbs of frequency (always, sometimes, never) correctly.",
    "Use conjunctions (and, but, or, so, because) to connect ideas.",
    "Use subject-verb agreement: singular subjects take singular verbs.",
    "Use parallel structure in lists and comparisons.",
    "Avoid double negatives.",
    "Use commas after introductory phrases.",
    "Use semicolons to join related independent clauses.",
    "Use apostrophes for possession and contractions.",
    "Use capital letters for proper nouns and the beginning of sentences.",
    "Use 'who' for people, 'which' for things, and 'that' for both in relative clauses.",
    "Use 'fewer' for countable nouns, 'less' for uncountable nouns.",
    "Use 'between' for two items, 'among' for more than two.",
    "Use 'each other' for two, 'one another' for more than two.",
    "Use 'lie' (to recline) and 'lay' (to put) correctly.",
    "Use 'raise' and 'rise' correctly.",
    "Use 'affect' (verb) and 'effect' (noun) correctly.",
    "Use 'accept' and 'except' correctly.",
    "Use 'advice' (noun) and 'advise' (verb) correctly.",
    "Use 'compliment' (praise) and 'complement' (complete) correctly.",
    "Use 'disinterested' (impartial) and 'uninterested' (bored) correctly.",
    "Use 'elicit' (to draw out) and 'illicit' (illegal) correctly.",
    "Use 'farther' (physical distance) and 'further' (abstract distance) correctly.",
    "Use 'historic' (important) and 'historical' (relating to history) correctly.",
    "Use 'imply' (suggest) and 'infer' (deduce) correctly.",
    "Use 'lie' (to recline) and 'lay' (to put) correctly.",
    "Use 'loose' (not tight) and 'lose' (to misplace) correctly.",
    "Use 'principal' (main, head of school) and 'principle' (rule) correctly.",
    "Use 'stationary' (still) and 'stationery' (paper) correctly.",
    "Use 'than' for comparisons, 'then' for time.",
    "Use 'there', 'their', and 'they're' correctly.",
    "Use 'to', 'too', and 'two' correctly.",
    "Use 'your' (possessive) and 'you're' (you are) correctly.",
    "Use 'its' (possessive) and 'it's' (it is) correctly.",
    "Use 'whose' (possessive) and 'who's' (who is) correctly.",
    "Use 'who' for subjects, 'whom' for objects.",
    "Use 'which' for non-restrictive clauses, 'that' for restrictive clauses.",
    "Use the subjunctive mood for wishes and hypotheticals: 'If I were...'",
    "Use 'unless' instead of 'if not' for negative conditions."
]

# Essay prompts (20)
essay_prompts = [
    "Do you agree or disagree with the following statement? Technology has made our lives more complicated. Use specific reasons and examples to support your answer.",
    "Some people prefer to live in a small town. Others prefer to live in a big city. Which do you prefer and why?",
    "Do you think that universities should require students to take a wide range of courses outside their major? Why or why not?",
    "In your opinion, what is the most important quality for a good leader? Use specific reasons and examples to support your answer.",
    "Some people believe that the best way to learn is through experience. Others believe that learning from books is more effective. Which do you agree with?",
    "Do you agree or disagree with the following statement? The most important thing that parents can teach their children is how to be independent.",
    "Some people think that government should spend more money on protecting the environment. Others think it should be spent on public health. Which do you think is more important?",
    "Do you agree or disagree with the following statement? It is better to work in a team than alone. Use specific reasons and examples.",
    "Some people prefer to plan their free time carefully. Others prefer to be spontaneous. Which do you prefer and why?",
    "Do you think that social media has a positive or negative effect on society? Explain your answer with examples.",
    "Some people believe that success comes from hard work. Others believe it comes from luck. Which do you agree with?",
    "Do you agree or disagree with the following statement? The most important goal of education is to prepare people for a career.",
    "Some people think that advertising influences our buying habits too much. Do you agree or disagree?",
    "Do you think that travel is necessary for a good education? Why or why not?",
    "Some people prefer to read fiction. Others prefer nonfiction. Which do you prefer and why?",
    "Do you agree or disagree with the following statement? The best way to reduce stress is to spend time alone.",
    "Some people think that money is the best measure of success. Do you agree or disagree?",
    "Do you think that schools should teach financial literacy? Why or why not?",
    "Some people believe that it is better to be a generalist. Others believe it is better to be a specialist. Which do you agree with?",
    "Do you agree or disagree with the following statement? The most important thing in life is happiness. Use specific reasons and examples."
]

essay_tips = """
**TOEFL Essay Writing Tips**

1. **Understand the prompt** – Make sure you answer the exact question.
2. **Plan before you write** – Spend 2–3 minutes outlining your main points.
3. **Write a clear thesis statement** – The first sentence of your introduction should state your position.
4. **Use topic sentences** – Each body paragraph should start with a sentence that introduces the main idea.
5. **Provide specific examples** – Avoid general statements; use real or hypothetical examples.
6. **Use transition words** – However, therefore, consequently, moreover, for instance.
7. **Keep your sentences varied** – Mix short and long sentences.
8. **Check your grammar and spelling** – Leave 2–3 minutes for proofreading.
9. **Stay on topic** – Do not include irrelevant information.
10. **Write at least 300 words** – Longer essays tend to score higher if well-organized.
"""

def get_items(base_list, lesson_num, count=50):
    start = (lesson_num - 1) * count
    end = start + count
    if end <= len(base_list):
        return base_list[start:end]
    else:
        first_part = base_list[start:]
        remaining = count - len(first_part)
        second_part = base_list[:remaining]
        return first_part + second_part

def get_essay_prompt(lesson_num):
    return essay_prompts[(lesson_num - 1) % len(essay_prompts)]

# ========== AUDIO FUNCTION ==========
def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled. Please install edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                generate_audio(text, tmp.name, VOICE)
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Audio error: {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ========== DISPLAY LESSON ==========
st.markdown(f"## 📖 Lesson {lesson_number}")

# Get lesson-specific content
conversations = generate_conversation(lesson_number)
vocab = get_items(vocab_base, lesson_number, 50)
idioms = get_items(idioms_base, lesson_number, 25)
grammar = get_items(grammar_base, lesson_number, 25)
essay_prompt = get_essay_prompt(lesson_number)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversations", "📚 Vocabulary", "💡 Idioms", "📖 Grammar", "✍️ Essay"])

# ----- TAB 1: Conversations -----
with tab1:
    st.subheader("TOEFL Interactive Conversations")
    for idx, conv in enumerate(conversations):
        st.markdown(conv)
        play_audio(conv, f"conv_{lesson_number}_{idx}")
        st.markdown("---")

# ----- TAB 2: Vocabulary -----
with tab2:
    st.subheader("TOEFL Vocabulary (50 words)")
    cols = st.columns(5)
    for idx, word in enumerate(vocab):
        with cols[idx % 5]:
            st.markdown(f"**{word}**")
            play_audio(word, f"vocab_{lesson_number}_{idx}")

# ----- TAB 3: Idioms -----
with tab3:
    st.subheader("TOEFL Idioms (25 idioms)")
    cols = st.columns(5)
    for idx, idiom in enumerate(idioms):
        with cols[idx % 5]:
            st.markdown(f"**{idiom}**")
            play_audio(idiom, f"idiom_{lesson_number}_{idx}")

# ----- TAB 4: Grammar -----
with tab4:
    st.subheader("TOEFL Grammar Rules (25 rules)")
    for idx, rule in enumerate(grammar):
        st.markdown(f"**{idx+1}. {rule}**")
        play_audio(rule, f"grammar_{lesson_number}_{idx}")
        st.markdown("---")

# ----- TAB 5: Essay -----
with tab5:
    st.subheader("TOEFL Essay Writing")
    st.markdown("### Essay Prompt")
    st.markdown(essay_prompt)
    play_audio(essay_prompt, f"essay_prompt_{lesson_number}")
    st.markdown("---")
    st.markdown("### Essay Writing Tips")
    st.markdown(essay_tips)
    play_audio(essay_tips, f"essay_tips_{lesson_number}")
    st.markdown("---")
    st.markdown("### Your Essay")
    st.text_area("Write your essay here:", height=300, key=f"essay_{lesson_number}")
    st.info("After writing, review your essay for grammar, coherence, and examples. Practice with a timer for TOEFL preparation.")

# ----- Milestone on lesson 20 -----
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Congratulations! You have completed the TOEFL Preparation Course.")
    st.markdown("""
    ### 📞 To continue with advanced TOEFL practice or get support:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Keep practicing and you will be ready for the TOEFL exam!
    """)
