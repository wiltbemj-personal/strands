#!/usr/bin/env python3
"""
Strands Puzzle Generator
Generates a self-contained HTML puzzle file from a YAML config.

Usage:
    python generate_puzzle.py puzzles/moms_birthday.yaml

Output:
    puzzles/moms_birthday.html  (or path set in config's 'output' key)
"""

import random
import json
import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not found. Install it with: conda install pyyaml")
    sys.exit(1)

ROWS = 6
COLS = 8
TOTAL_CELLS = ROWS * COLS

# Weighted letter pool for filling empty grid cells
FILL_LETTERS = (
    "E" * 12 + "T" * 9 + "A" * 8 + "O" * 8 + "I" * 7 + "N" * 6 +
    "S" * 6 + "H" * 6 + "R" * 6 + "D" * 4 + "L" * 4 + "C" * 3 +
    "U" * 3 + "M" * 2 + "W" * 2 + "F" * 2 + "G" * 2 + "Y" * 2 +
    "P" * 2 + "B" + "V" + "K" + "J" + "X" + "Q" + "Z"
)

# Built-in common English words (3–8 letters) for hint detection.
# Add more to words/common_words.txt to extend this list.
BUILTIN_WORDS = set("""
ace act add age ago aid aim air ale all ant ape apt arc are ark arm art ash ask ate
awe axe aye bad bag ban bar bat bay bed beg bet bid big bit bow box boy bud bug bun
bus but buy cab can cap car cat cob cod cog cop cot cow cub cup cut dab dam dew did
dig dim dip doe dog dot dry dub dud dug dye ear eat egg elf elk elm emu end era eve
ewe eye fad fan far fat fax foe fog for fox fry fun fur gag gap gas gay gel gem get
gig gnu god got gum gun gut guy gym had ham has hat haw hay hem hen her hew hid him
his hit hob hoe hog hop how hub hue hug hum hut ice ilk imp ink ion ire ivy jab jag
jam jar jaw jay jet jig job jot joy jug jut keg kid kin kit lag lap law lax lay led
leg let lid lip lit log low lug mad man map mar mat maw may men met mob mod mom mop
mud mug nag nap nip nit nod nor not now nun oak oar odd ode off oft oil old orb ore
our out owe owl own pad pal pan paw pay peg pen pep pet pie pig pin pit ply pod pop
pot pow pro pub pun pup pus put rag ram ran rap rat raw ray red ref rep rev rib rid
rig rip rob rod rot row rub rut rye sac sad sag sap sat saw say sea set sew shy sin
sip sir sit ski sky sly sob sod son sow soy spa spy sty sub sue sum sun sup tab tan
tap tar tax tea ten the tie tin tip toe too top tow toy try tub tug two urn use van
vat via vie vim vow wag war was wax way web wed who why wig win woe wok won woo yak
yam yap yaw yep yet you zap zen zip zoo able ache acid aged also alto arch area aria
army aunt back bade bail bale ball balm band bane bang bank barn base bash bask bast
bath bead beak beam bean beat been beet bell belt bend best bias bike bill bind bite
bled blew blob bloc blot blow blue blur boar boat body bold bolt bond bone book boom
boon boot bore born bout bowl brag bran brat brew brim brow buck bulk bull bump bunk
bunt buoy burn burp burr bury bush busy buzz cage cake call calm came cane cape card
care cart case cash cast cave cell cent chap char chat chef chew chin chip chop chow
clad clam clan clap claw clay clef clip clog clop clot club clue coal coat coil coin
cold colt come cone cook cool cope cord core cork corn cost cozy cram craw crew crop
crow crud crux cube cuff cure curl curt cute damp dare dark darn dart dash data date
dawn days dead deaf deal dean dear deed deem deep dell dent desk dice diet dill dime
dine ding dire disk dive dock dome done door dote dove down drab drag drip drop drug
drum duel duet dull dune dunk dusk dust duty each earn ease east edge else emit epic
even ever evil exam exam face fade fail fair fake fall fame fang fare farm fast fate
fawn faze feat feed feel feet fell felt fend feud fife file fill film find fine fire
firm fish fist five flag flak flat flaw flea fled flex flip flit flock flop flow foam
foci fold folk fond font fool ford fore fork form fort foul four fowl fray free fret
from fuel full fume fund fury fuse fuss gain gale gall gash gave gaze geld gent gift
gild gill gist give glad glee glen glib glop glow glue gnat goad goat gold golf gone
good gore gory gown grab gram grin grip grit grow grub gulf gull gulp gust guts gyms
hack half hall halt hand hang hard hare harm harp hash haste hate haul have hawk haze
head heal heap hear heat heel held helm help herb herd hero hide high hike hill hint
hire hive hoax hole holy home hood hoof hook hope horn host hour howl hull hulk hung
hunt hurt husk hymn icon idle illy inch into iris isle itch item jade jail jest jibe
join joke jolt junk just keen keep keel kept kick kind king knee knew knob knot know
lace lack laid lake lame lamp lane lard lark lash last late laud lawn lead leaf lean
leap left lend lens lent lest levy liar lied lien lieu like lime limp line link lint
lion lire list live load loaf loam loan lock loft lone long loom loon loop lore lore
lorn lore lose loss loft loud lout love lull lure lurk lush lust luxe made maid main
make male mall malt mane mare mark mart mast mate math maze mead meal mean meet meld
melt memo mend mere mesh mild mile mill mime mine mint mire miss mist moan moat mock
mode mold mole molt monk mood moor moot more morn mort most moth move much muck mull
muse musk must myth nail name nape narc nark nave navy near neat need neon nest next
nice nick nigh node none noon norm nose note noun numb oafs obey odor okay omen omit
once only onto open orca oven over owed oxen pace pack pact page paid pain pair pale
palm pang pant park part pass past path pave pawl peak peal peat peck peel peer pelt
perk pest pick pier pile pill pity plan play plod plop plot plow ploy plug plum plus
poem poet poll polo pond pony pool poor pope pore pork port pose posh post pour pout
pray prep prey prig prim prod prop prow pull pump punk pure push quay quit race rack
rain rake ramp rang rank rant rape rash rate rave rays ream reap rein rely rend rent
rest rice rich ride rife rift ring riot robe role roll romp roof rook room root rope
rose rosy rout rove ruin rule ruse rush rust sage sail sale salt same sand sane sang
sank sash save scan scar seal seam sear seed seek self sell semi send sent serf shed
shin ship shot show sick side sigh silk sill silt sire site size skim skip slab slag
slam slap slat slaw sled slew slid slim slip slot slow slug slum slur smog snap snob
snug soak soar sock sofa soft soil sold sole some song soot sore sort soul span spat
spin spit spot spun spur stab stag star stay stem step stew stir stop stow stub stud
such suit sulk sung sunk sure swab swam swan swap swat swum tack tail tale talk tall
tame tang tank tape tart task teal team teem tell tend term test text than that them
then they thin tide tied till time tiny tire toad toil told toll tome tong took torn
toss tour town trap tray tree trim trio trip trod trot true tune turf turn twig type
ugly upon used vain vale vane vary vast veil vein vend very vest veto view vile vine
visa void vote wade wail wait walk wall wand wane ward ware warm warp wars wart wary
wash wasp wave weak weal wean weed weep weld well welt went west when whim whip wile
will wilt wily wind wine wing wink wiry wish wisp wits wolf womb wood word wore worm
worn wove writ yell yore zeal zone ability ablaze abrupt access affair afford afraid
after again agate agile aging aisle alarm algae alien align alley allow alloy along
alone alter amaze amble amend ample amuse angel angry annex antic anvil aorta apple
apply apron aptly ardor arena argue arise array aside askew assay atlas atone attic
audio avail avert avoid await awake awash awful awoke axial abyss abide about above
abuse ached acres acute added admit adult after again agony ahead aided aimed aired
album alert aloft alone along aloof aloud altar amiss among ample angel angry anime
ankle annoy antic apart aphid apron aptly arcane ardor argue arson aside asked aspen
asset attic audio avail avert avid avoid awake awful ached aided aimed alert alive
allow alone aloof alter angel angry ankle annex apron arise armor array aside asset
atone awake awful axial azure badge badly bagel baked baker baler balls balsa banal
banjo baron basic basis batch bathe baton bauble beach beady beard beast bedew begat
beige belle below bench berry bevel binge birch birth black blade blame bland blank
blast blaze bleak bleat bleed blend bless blind bliss block blood bloom blown blunt
blurb blush board boast boggy bolts bonus booty borax botch bound boxer braid brain
brake brand brash brave brawl braze brazen breed breve bride brief brine brink brisk
broad broil broke brood broth brown brows brush brusk brute budge buggy built bulge
buoy burgh bushy cable camel candy canny canoe canon caper caput cargo carol carry
cause chafe chair chalk champ chant chaos chard charm chase cheap cheat check cheek
cheep cheer chess chest chide child chill chirp choir chord chose chunk civic civil
clack claim clang clash clasp cleat cleft clerk click clime clink clock clone close
cloth cloud clout clown coarsen cobra coils coins color comet comic comma conch condo
could court cover craft cramp crane creak cream creek crest crimp crisp cross crowd
crown crude cruel crumb crush crust crypt curly curve daily dairy daisy dance dared
daunt dealt debut decal decay decoy decry delta depot depth derby devil dewdrop diary
digit dingo dirty disco ditty dizzy dodge doing dolly draft drain drake drape drawl
drawn dread dream dregs drift drink drive droit drove drown drove droop drove dryer
duchy dummy dunce duple dusty dwarf dwell dying eager eagle early earthy eaten ebony
eclat edema edged edict eerie eight eject elite elope embed emery empty enact endow
enemy enjoy ensue entry envoy equip error essay etude evade event every evict evoke
exact exalt exact exert exile exist expel extol extra fable facet faint faith false
fancy farce fatal feast feeble feral fetch fever fewer fiber field fiend fifth fifty
fifty fight filmy final finer first fishy fixed fjord flame flare flash flask flaunt
fleet flesh flick flier flock floor flora floss flour flout flown fluff fluid fluke
flume flung flunk flute flyer foamy focal folly force forge forge forgo forme forth
found foyer frail frame franc frank fraud freak freed fresh froze frugal fruit frump
fully funky funny fuzzy gaily garb gaudy gauge gauze given gizmo glair gland glare
glaze gleam glean glide glint gloat globe gloom glory gloss glove glyph grace grade
graft grail grain grasp grassy gravel graze greed green greet groan groin groom group
grove growl gruel gruff guard guile guise gusto gusty gypsy habit harsh haste hasty
haven hazel heady heart heavy hefty hence herbs helix hence hilly hippo hoist holly
homer honor hopeful hornet hotel hound hover human humor humus hunch hurry husky
hypno icing ideal idiom igloo image imply incur indie infer inner input inter intro
irate issue itchy ivory jaunt jazzy jewel jiffy joust juice juicy jumbo jumpy kayak
kinky kitty klutz knack knave kneel knelt knife knoll known koala label large later
lathe lofty light limit linen liner lithe liver livid loony lover lowly lucid lucky
lunar lunch lusty lying lyric magic major maker mambo mania manor maple march marry
marsh massy match maybe mealy meaty melon mercy mercy merci messy metal meter might
milky minty mirky mixed mixer model mogul moist money month moody moose mourn mouse
muddy muggy mulch mummy murky musty mushy mucky nasal nasty naval needy never newly
ninja ninety noble noisy north notch novel novel novice nudge nurse nutty nymph occur
octet offal often olive onion onyx opera optic orbit orchid order organ other otter
ought outer outdo outgo outrun outset ovary ovoid owing oxide ozone paddy pagan pansy
party pasta patch patio patsy paved peach pedal penal penny perch peril perky perky
petty phase phone photo piano picky pilot pinch piney pinky pirate pitch pithy pixie
pizza place plaid plain plane plank plant plasm plaza plead pleat plumb plume plump
plunk plush poker polar polka pooch poppy porky prank press pride prime primp prism
prize probe prong proof prose proud prowl prude prune psalm pudgy pulse puffy pulse
pully pulpy punch pupil puny purse query queue quick quiet quirk quota quote rabbi
rainy rally ramen ranch rangy rapid raspy ratio ratty raven rayon razed reach ready
realm rebus rebel rebus recur reedy regal reign relax repay repel repay repel repay
reply retro retry reuse revel ripen risky rivet rivet roast robot rocky rodeo rouge
rough round rouse rowdy royal ruddy rugby ruler runic rusty sadly saint salty sandy
sappy saucy sauce savvy savor scalp scaly scamp scant scary scene scoff scone scoop
scorch score scorn scout scowl scram scrap screw scrub seedy sense serum seven shack
shade shady shaft shaky shale shall shame shape share sharp shave shawl sheep sheer
sheet shelf shell shift shiny shirk shock shore short shout shove showy shrub shrug
shuck shunt shush since sinew sixth sixty sixty skate sketchy skill skimp skirt skirm
slack slain slake slang slash sleek sleep sleet slew slice slide slime slimy slope
slosh sloth slunk slurp small smack smart smash smear smell smelt smile smirk smite
smith smock smoke smoky snack snail snake snare snark sneak sneer sniff snore snowy
snuck soggy solar solve sonic sorry south sovereign space spade spare spark spawn
spear speck speed spell spice spill spine spire splash splat spleen spoil spoke spook
spool spoon sport spout spray squad squat squib squid stain stale stall stank stare
stark stark stark start start stash stave steal steam steel steed steep steer stein
stern stoic stomp stony stool stood storm story stout stove straw stray strip strut
stuck study stump stung stunk style suave sugar suite sultry sumac sunny sunny super
surge surly swamp swear sweat sweep sweet swell swept swill swipe swirl swoon sword
syrup tabby tacky taffy tangy tapir taunt taupe tawny taffy tense tepid thank thick
thorn those three threw throw thumb tidal tidal tiger tight tilde tinge tipsy tired
today tonal tonic tooth topaz touch tough towel toxic trail train trait tramp trout
trove truck truly trump truss truth tulip tumor tunic tutor tweed tweet twice twill
twirl twist tying udder ulcer ultra uncut under unfit union unite until upper upset
urban usage usher utter vague vapor vault vaunt vigor viper viral visor vista vivid
vocal vogue vowed vowel vulva waltz wacky weary weedy weird whack whale whiff whole
whose widen wider wimpy windy witty woken wordy worse worst worth would wrath wreak
wring wrist wrong wrote yacht yearn zesty zippy zombie
""".split())


# ── Grid generation ───────────────────────────────────────────────────────────

def place_word(word: str, occupied: set, span_left=False, span_right=False):
    """
    Backtracking placement: find a connected path of empty cells for `word`.
    Returns list of (r, c) tuples or None if no placement found.
    span_left/span_right: path must include a cell in col 0 / col COLS-1.
    """
    word = word.upper()
    n = len(word)

    def bt(idx, r, c, path, path_set, left, right):
        left = left or (c == 0)
        right = right or (c == COLS - 1)
        if idx == n:
            if span_left and not left:
                return None
            if span_right and not right:
                return None
            return list(path)
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (0 <= nr < ROWS and 0 <= nc < COLS
                    and (nr, nc) not in occupied
                    and (nr, nc) not in path_set):
                path.append((nr, nc))
                path_set.add((nr, nc))
                result = bt(idx + 1, nr, nc, path, path_set, left, right)
                if result:
                    return result
                path.pop()
                path_set.remove((nr, nc))
        return None

    if span_left:
        starts = [(r, 0) for r in range(ROWS) if (r, 0) not in occupied]
    elif span_right:
        starts = [(r, COLS - 1) for r in range(ROWS) if (r, COLS - 1) not in occupied]
    else:
        starts = [(r, c) for r in range(ROWS) for c in range(COLS)
                  if (r, c) not in occupied]

    random.shuffle(starts)
    for r, c in starts:
        result = bt(1, r, c, [(r, c)], {(r, c)}, c == 0, c == COLS - 1)
        if result:
            return result
    return None


def generate_puzzle(theme_words: list, spangram: str, max_attempts=2000):
    """
    Place spangram + theme words on a 6×8 grid.
    Returns (grid, placements, attempts_used).
    placements: dict mapping word (or '__spangram__') → [(r,c), ...]
    """
    words = [w.upper() for w in theme_words]
    sp = spangram.upper()
    total_letters = sum(len(w) for w in words) + len(sp)

    if total_letters != TOTAL_CELLS:
        diff = TOTAL_CELLS - total_letters
        direction = "add" if diff > 0 else "remove"
        raise ValueError(
            f"Words total {total_letters} letters but the grid has exactly "
            f"{TOTAL_CELLS} cells ({ROWS}×{COLS}). Every cell must belong to a word "
            f"(no random fill letters), so {direction} {abs(diff)} letter(s) "
            f"across your words or spangram."
        )

    print(f"  Grid: {ROWS}×{COLS} = {TOTAL_CELLS} cells")
    print(f"  Word letters: {total_letters} (exact fit, no fill letters needed)")

    for attempt in range(1, max_attempts + 1):
        occupied: set = set()
        placements: dict = {}

        # Place spangram first (must touch both left and right edges)
        sp_path = place_word(sp, occupied, span_left=True, span_right=True)
        if not sp_path:
            continue
        for cell in sp_path:
            occupied.add(cell)
        placements['__spangram__'] = sp_path

        # Place theme words in random order
        word_list = words[:]
        random.shuffle(word_list)
        ok = True
        for w in word_list:
            path = place_word(w, occupied)
            if not path:
                ok = False
                break
            for cell in path:
                occupied.add(cell)
            placements[w] = path

        if not ok:
            continue

        # Build the character grid
        grid = [['' for _ in range(COLS)] for _ in range(ROWS)]
        for key, path in placements.items():
            actual = sp if key == '__spangram__' else key
            for i, (r, c) in enumerate(path):
                grid[r][c] = actual[i]

        # Fill empty cells with weighted random letters
        for r in range(ROWS):
            for c in range(COLS):
                if not grid[r][c]:
                    grid[r][c] = random.choice(FILL_LETTERS)

        print(f"  Placed all words in {attempt} attempt(s).")
        return grid, placements, attempt

    raise ValueError(
        f"Could not place all words after {max_attempts} attempts.\n"
        "Tips: use shorter words, fewer words, or run the script again (placement is random)."
    )


# ── Common word list ──────────────────────────────────────────────────────────

def load_common_words() -> list:
    """Load word list from file if present, otherwise use built-in set."""
    words_file = Path(__file__).parent / 'words' / 'common_words.txt'
    if words_file.exists():
        extra = set(
            w.strip().upper()
            for w in words_file.read_text().splitlines()
            if 3 <= len(w.strip()) <= 8 and w.strip().isalpha()
        )
        return sorted({w.upper() for w in BUILTIN_WORDS} | extra)
    return sorted(w.upper() for w in BUILTIN_WORDS)


# ── HTML rendering ────────────────────────────────────────────────────────────

def render_html(grid, placements, theme, spangram, theme_words, author='', date='') -> str:
    sp = spangram.upper()

    word_data = {}
    for key, path in placements.items():
        word = sp if key == '__spangram__' else key
        word_data[word] = {'cells': path, 'is_spangram': key == '__spangram__'}

    puzzle = {
        'theme': theme,
        'grid': grid,
        'words': word_data,
        'spangram': sp,
        'author': author,
        'date': date,
    }

    common_words = load_common_words()
    # Remove theme words from the hint-word pool so they can't be "found" early
    theme_set = {w.upper() for w in theme_words} | {sp}
    common_words = [w for w in common_words if w not in theme_set]

    puzzle_json = json.dumps(puzzle)
    common_words_json = json.dumps(common_words)

    return HTML_TEMPLATE.replace('__PUZZLE_JSON__', puzzle_json) \
                        .replace('__COMMON_WORDS_JSON__', common_words_json)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Generate a Strands puzzle HTML file.')
    parser.add_argument('config', help='Path to YAML puzzle config file')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducible layout')
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: config file not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    theme = config.get('theme', 'Strands')
    spangram = config.get('spangram', '').strip()
    words = [w.strip() for w in config.get('words', [])]
    author = config.get('author', '')
    date = config.get('date', '')

    if not spangram:
        print("Error: 'spangram' is required in the config.")
        sys.exit(1)
    if not words:
        print("Error: 'words' list is required in the config.")
        sys.exit(1)

    # Default output: same dir as config, same stem, .html extension
    if 'output' in config:
        out_path = Path(config['output'])
    else:
        out_path = config_path.with_suffix('.html')

    if args.seed is not None:
        random.seed(args.seed)

    print(f"\nGenerating puzzle: \"{theme}\"")
    print(f"  Spangram : {spangram.upper()}")
    print(f"  Words    : {', '.join(w.upper() for w in words)}")

    grid, placements, attempts = generate_puzzle(words, spangram)
    html = render_html(grid, placements, theme, spangram, words, author, date)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f"\n✓ Puzzle written to: {out_path}")
    print(f"  Open it in a browser or push to GitHub Pages to share.")


# ── HTML Template ─────────────────────────────────────────────────────────────
# __PUZZLE_JSON__ and __COMMON_WORDS_JSON__ are replaced at render time.

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Strands Puzzle</title>
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0; padding: 0;
      -webkit-tap-highlight-color: transparent;
    }
    :root {
      --blue: #4a90e2;
      --gold: #e8a020;
      --bg: #faf8f4;
      --surface: #ffffff;
      --cell-bg: #e4ddd3;
      --cell-sel: #aecff5;
      --text: #1a1a1a;
      --muted: #888;
      --border: #e0d8cc;
    }
    html, body {
      height: 100%;
      overscroll-behavior: none;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      display: flex;
      flex-direction: column;
      align-items: center;
      touch-action: none;
    }

    /* ── Header ── */
    header {
      width: 100%;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 10px 16px 8px;
      text-align: center;
    }
    .game-eyebrow {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 3px;
    }
    .game-theme {
      font-size: 20px;
      font-weight: 800;
      color: var(--text);
      line-height: 1.2;
    }
    .game-hint-line {
      font-size: 12px;
      color: var(--muted);
      margin-top: 2px;
    }

    /* ── Game container ── */
    .game-wrap {
      width: 100%;
      max-width: 480px;
      padding: 10px 10px 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }

    /* ── Hint bar ── */
    .hint-row {
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      justify-content: center;
      min-height: 36px;
    }
    .hint-dots {
      display: flex;
      gap: 5px;
      align-items: center;
    }
    .hint-dot {
      width: 11px; height: 11px;
      border-radius: 50%;
      background: #d0c8be;
      transition: background 0.25s;
    }
    .hint-dot.lit { background: var(--blue); }
    .hint-btn {
      border: none;
      background: var(--text);
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      padding: 6px 18px;
      border-radius: 999px;
      cursor: pointer;
      transition: opacity 0.2s;
      letter-spacing: 0.3px;
    }
    .hint-btn:disabled {
      background: #ccc;
      cursor: default;
    }
    .hint-count {
      font-size: 12px;
      color: var(--muted);
      min-width: 70px;
    }

    /* ── Message bar ── */
    .msg-bar {
      min-height: 24px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
      text-align: center;
      transition: opacity 0.3s;
    }

    /* ── Grid ── */
    .grid-wrap {
      position: relative;
      width: 100%;
      /* maintain 8:6 aspect ratio */
      aspect-ratio: 8 / 6;
    }
    #the-grid {
      position: absolute;
      inset: 0;
      display: grid;
      grid-template-columns: repeat(8, 1fr);
      gap: clamp(3px, 1.2vw, 6px);
      padding: clamp(2px, 0.8vw, 4px);
    }
    .cell {
      border-radius: 50%;
      background: var(--cell-bg);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: clamp(11px, 3.4vw, 17px);
      font-weight: 800;
      color: var(--text);
      cursor: pointer;
      user-select: none;
      touch-action: none;
      transition: background 0.12s, transform 0.1s;
      will-change: background;
    }
    .cell.sel {
      background: var(--cell-sel);
      transform: scale(1.1);
      z-index: 2;
      position: relative;
    }
    .cell.found-theme   { background: var(--blue); color: #fff; }
    .cell.found-spangram { background: var(--gold); color: #fff; }

    @keyframes shake {
      0%,100% { transform: translateX(0); }
      20%      { transform: translateX(-5px); }
      40%      { transform: translateX(5px); }
      60%      { transform: translateX(-4px); }
      80%      { transform: translateX(4px); }
    }
    @keyframes nonThemeFlash {
      0%,100% { background: var(--cell-bg); }
      40%     { background: #9ee09e; transform: scale(1.08); }
    }
    @keyframes hintPulse {
      0%,100% { background: var(--cell-bg); }
      30%,70% { background: #ffe066; transform: scale(1.12); }
    }
    @keyframes foundPop {
      0%   { transform: scale(0.7); opacity: 0; }
      60%  { transform: scale(1.15); }
      100% { transform: scale(1); opacity: 1; }
    }
    .shake        { animation: shake 0.38s; }
    .non-flash    { animation: nonThemeFlash 0.55s; }
    .hint-pulse   { animation: hintPulse 1.4s ease-in-out; }

    /* SVG connector overlay */
    #conn-svg {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 3;
      overflow: visible;
    }

    /* ── Found words ── */
    .found-section { width: 100%; }
    .found-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--muted);
      text-align: center;
      margin-bottom: 7px;
    }
    .found-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      justify-content: center;
    }
    .chip {
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.4px;
      animation: foundPop 0.35s cubic-bezier(.34,1.56,.64,1);
    }
    .chip.theme    { background: var(--blue); color: #fff; }
    .chip.spangram { background: var(--gold); color: #fff; }

    /* ── Win overlay ── */
    #win-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,.65);
      z-index: 50;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    #win-overlay.show { display: flex; }
    .win-card {
      background: #fff;
      border-radius: 22px;
      padding: 28px 22px 22px;
      max-width: 320px;
      width: 100%;
      text-align: center;
      animation: foundPop 0.4s cubic-bezier(.34,1.56,.64,1);
    }
    .win-emoji { font-size: 52px; margin-bottom: 10px; }
    .win-title { font-size: 26px; font-weight: 800; color: var(--text); }
    .win-sub   { font-size: 14px; color: var(--muted); margin: 6px 0 14px; line-height: 1.5; }
    .win-stats {
      background: #f5f2ee;
      border-radius: 12px;
      padding: 12px 16px;
      font-size: 14px;
      color: #444;
      line-height: 1.8;
      margin-bottom: 14px;
    }
    .share-btn {
      width: 100%;
      border: none;
      background: var(--text);
      color: #fff;
      font-size: 16px;
      font-weight: 700;
      padding: 13px;
      border-radius: 999px;
      cursor: pointer;
    }
  </style>
</head>
<body>

<header>
  <div class="game-eyebrow">Strands</div>
  <div class="game-theme" id="game-theme"></div>
  <div class="game-hint-line">Find all the words that fit the theme</div>
</header>

<div class="game-wrap">

  <div class="hint-row">
    <div class="hint-dots" id="hint-dots"></div>
    <button class="hint-btn" id="hint-btn" disabled>Hint</button>
    <span class="hint-count" id="hint-count"></span>
  </div>

  <div class="msg-bar" id="msg-bar"></div>

  <div class="grid-wrap" id="grid-wrap">
    <svg id="conn-svg"></svg>
    <div id="the-grid"></div>
  </div>

  <div class="found-section" id="found-section" style="display:none">
    <div class="found-label">Found</div>
    <div class="found-chips" id="found-chips"></div>
  </div>

</div>

<div id="win-overlay">
  <div class="win-card">
    <div class="win-emoji">🎉</div>
    <div class="win-title">Puzzle solved!</div>
    <div class="win-sub" id="win-sub"></div>
    <div class="win-stats" id="win-stats"></div>
    <button class="share-btn" id="share-btn">Share Result</button>
  </div>
</div>

<script>
const PUZZLE = __PUZZLE_JSON__;
const WORD_SET = new Set(__COMMON_WORDS_JSON__);

// ── Constants ────────────────────────────────────────────────────────────────
const ROWS = 6, COLS = 8;
const CREDITS_PER_HINT = 3;

// ── State ────────────────────────────────────────────────────────────────────
const S = {
  sel: [],            // [{r,c}] currently selected
  dragging: false,
  foundWords: new Set(),
  foundCells: new Set(),   // "r,c"
  hintCredits: 0,
  hintsUsed: 0,
  startTime: Date.now(),
};

// ── DOM ──────────────────────────────────────────────────────────────────────
const gridEl      = document.getElementById('the-grid');
const svgEl       = document.getElementById('conn-svg');
const hintDotsEl  = document.getElementById('hint-dots');
const hintBtn     = document.getElementById('hint-btn');
const hintCount   = document.getElementById('hint-count');
const msgBar      = document.getElementById('msg-bar');
const foundSec    = document.getElementById('found-section');
const foundChips  = document.getElementById('found-chips');
const winOverlay  = document.getElementById('win-overlay');
const shareBtn    = document.getElementById('share-btn');

document.getElementById('game-theme').textContent = PUZZLE.theme;

// ── Build cell lookup ────────────────────────────────────────────────────────
// word → Set of "r,c"  (for display after found)
const wordCellMap = {};
for (const [w, d] of Object.entries(PUZZLE.words)) {
  wordCellMap[w] = new Set(d.cells.map(([r,c]) => `${r},${c}`));
}
const totalWords = Object.keys(PUZZLE.words).length;

// ── Render grid ──────────────────────────────────────────────────────────────
const cellEls = {};  // "r,c" → element

(function buildGrid() {
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const el = document.createElement('div');
      el.className = 'cell';
      el.textContent = PUZZLE.grid[r][c];
      el.dataset.r = r;
      el.dataset.c = c;
      gridEl.appendChild(el);
      cellEls[`${r},${c}`] = el;
    }
  }
})();

// ── Pointer interaction ───────────────────────────────────────────────────────
function cellAt(x, y) {
  let el = document.elementFromPoint(x, y);
  if (!el) return null;
  if (!el.classList.contains('cell') && el.parentElement && el.parentElement.classList.contains('cell'))
    el = el.parentElement;
  return el.classList.contains('cell') ? el : null;
}

function key(el) { return `${el.dataset.r},${el.dataset.c}`; }

function adjacent(a, b) {
  return Math.abs(+a.dataset.r - +b.dataset.r) <= 1 &&
         Math.abs(+a.dataset.c - +b.dataset.c) <= 1 &&
         a !== b;
}

function lastSelEl() {
  if (!S.sel.length) return null;
  const {r,c} = S.sel[S.sel.length-1];
  return cellEls[`${r},${c}`];
}

gridEl.addEventListener('pointerdown', e => {
  const el = cellAt(e.clientX, e.clientY);
  if (!el || S.foundCells.has(key(el))) return;
  e.preventDefault();
  S.dragging = true;
  S.sel = [{r: +el.dataset.r, c: +el.dataset.c}];
  el.setPointerCapture(e.pointerId);
  refreshCells();
  drawConnector();
});

gridEl.addEventListener('pointermove', e => {
  if (!S.dragging) return;
  e.preventDefault();
  const el = cellAt(e.clientX, e.clientY);
  if (!el || S.foundCells.has(key(el))) return;
  const last = lastSelEl();
  if (!last) return;

  const existIdx = S.sel.findIndex(c => c.r == +el.dataset.r && c.c == +el.dataset.c);
  if (existIdx >= 0) {
    // Allow backtracking
    if (existIdx < S.sel.length - 1) {
      S.sel = S.sel.slice(0, existIdx + 1);
      refreshCells();
      drawConnector();
    }
  } else if (adjacent(last, el)) {
    S.sel.push({r: +el.dataset.r, c: +el.dataset.c});
    refreshCells();
    drawConnector();
  }
});

window.addEventListener('pointerup',     () => { if (S.dragging) { S.dragging = false; submit(); } });
window.addEventListener('pointercancel', () => { S.dragging = false; clearSel(); });

// ── Selection helpers ─────────────────────────────────────────────────────────
function clearSel() { S.sel = []; refreshCells(); drawConnector(); }

function refreshCells() {
  const selSet = new Set(S.sel.map(({r,c}) => `${r},${c}`));
  for (const [k, el] of Object.entries(cellEls)) {
    el.classList.toggle('sel', selSet.has(k) && !S.foundCells.has(k));
  }
}

function selWord() {
  return S.sel.map(({r,c}) => PUZZLE.grid[r][c]).join('');
}

// ── Submission ────────────────────────────────────────────────────────────────
function submit() {
  if (S.sel.length < 3) { clearSel(); return; }

  const word = selWord();

  // Theme word match
  if (PUZZLE.words[word] && !S.foundWords.has(word)) {
    const isSpangram = PUZZLE.words[word].is_spangram;
    markFound(word, isSpangram);
    clearSel();
    return;
  }

  // Non-theme dictionary word → hint credit
  if (WORD_SET.has(word) && !S.foundWords.has(word)) {
    nonThemeFound(word);
    return;
  }

  // Wrong
  animateCells(S.sel.map(({r,c}) => cellEls[`${r},${c}`]), 'shake', 380);
  clearSel();
}

function markFound(word, isSpangram) {
  S.foundWords.add(word);
  for (const [r,c] of PUZZLE.words[word].cells) {
    const k = `${r},${c}`;
    S.foundCells.add(k);
    const el = cellEls[k];
    el.classList.remove('sel');
    el.classList.add(isSpangram ? 'found-spangram' : 'found-theme');
  }
  showMsg(isSpangram ? '✨ Spangram!' : '🎯 ' + cap(word));
  addChip(word, isSpangram);
  drawConnector();
  if (S.foundWords.size === totalWords) setTimeout(showWin, 700);
}

function nonThemeFound(word) {
  S.foundWords.add(word);
  S.hintCredits++;
  const cells = S.sel.map(({r,c}) => cellEls[`${r},${c}`]);
  animateCells(cells, 'non-flash', 560);
  showMsg(`"${cap(word)}" +1 hint credit`);
  refreshHintUI();
  setTimeout(clearSel, 80);
}

function animateCells(els, cls, duration) {
  for (const el of els) {
    el.classList.remove(cls);
    void el.offsetWidth; // reflow to restart animation
    el.classList.add(cls);
    setTimeout(() => el.classList.remove(cls), duration);
  }
}

// ── Hints ─────────────────────────────────────────────────────────────────────
function refreshHintUI() {
  const avail = Math.floor(S.hintCredits / CREDITS_PER_HINT);
  const rem   = S.hintCredits % CREDITS_PER_HINT;

  hintDotsEl.innerHTML = '';
  for (let i = 0; i < CREDITS_PER_HINT; i++) {
    const d = document.createElement('div');
    d.className = 'hint-dot' + (i < rem ? ' lit' : '');
    hintDotsEl.appendChild(d);
  }
  hintBtn.disabled = avail === 0;
  hintCount.textContent = avail > 0 ? `${avail} hint${avail > 1 ? 's' : ''}` : '';
}

hintBtn.addEventListener('click', () => {
  const avail = Math.floor(S.hintCredits / CREDITS_PER_HINT);
  if (avail === 0) return;

  const unfound = Object.entries(PUZZLE.words).filter(([w]) => !S.foundWords.has(w));
  if (!unfound.length) return;

  S.hintCredits -= CREDITS_PER_HINT;
  S.hintsUsed++;
  refreshHintUI();

  const [word, data] = unfound[Math.floor(Math.random() * unfound.length)];
  const cells = data.cells.map(([r,c]) => cellEls[`${r},${c}`]);
  animateCells(cells, 'hint-pulse', 1400);
  showMsg(`Hint: look for "${cap(word)}"`);
});

// ── SVG connector ─────────────────────────────────────────────────────────────
function drawConnector() {
  svgEl.innerHTML = '';
  if (S.sel.length < 2) return;

  const wRect = document.getElementById('grid-wrap').getBoundingClientRect();
  const pts = S.sel.map(({r,c}) => {
    const rect = cellEls[`${r},${c}`].getBoundingClientRect();
    return { x: rect.left + rect.width/2 - wRect.left,
             y: rect.top  + rect.height/2 - wRect.top };
  });

  const ns = 'http://www.w3.org/2000/svg';

  const line = document.createElementNS(ns, 'polyline');
  line.setAttribute('points', pts.map(p=>`${p.x},${p.y}`).join(' '));
  line.setAttribute('fill', 'none');
  line.setAttribute('stroke', '#4a90e2');
  line.setAttribute('stroke-width', '4');
  line.setAttribute('stroke-linecap', 'round');
  line.setAttribute('stroke-linejoin', 'round');
  line.setAttribute('opacity', '0.65');
  svgEl.appendChild(line);

  for (const p of pts) {
    const circle = document.createElementNS(ns, 'circle');
    circle.setAttribute('cx', p.x);
    circle.setAttribute('cy', p.y);
    circle.setAttribute('r', '5');
    circle.setAttribute('fill', '#4a90e2');
    circle.setAttribute('opacity', '0.75');
    svgEl.appendChild(circle);
  }
}

// ── Found chips ───────────────────────────────────────────────────────────────
function addChip(word, isSpangram) {
  foundSec.style.display = '';
  const chip = document.createElement('div');
  chip.className = 'chip ' + (isSpangram ? 'spangram' : 'theme');
  chip.textContent = cap(word);
  foundChips.appendChild(chip);
}

// ── Message bar ───────────────────────────────────────────────────────────────
let msgTimer;
function showMsg(text) {
  msgBar.textContent = text;
  clearTimeout(msgTimer);
  msgTimer = setTimeout(() => { msgBar.textContent = ''; }, 3200);
}

// ── Win screen ────────────────────────────────────────────────────────────────
function showWin() {
  const secs = Math.floor((Date.now() - S.startTime) / 1000);
  const t = secs >= 60 ? `${Math.floor(secs/60)}m ${secs%60}s` : `${secs}s`;
  document.getElementById('win-sub').textContent =
    `You found all the words for "${PUZZLE.theme}"`;
  document.getElementById('win-stats').innerHTML =
    `<strong>Time:</strong> ${t}<br><strong>Hints used:</strong> ${S.hintsUsed}`;
  winOverlay.classList.add('show');
  confetti();
}

shareBtn.addEventListener('click', () => {
  const secs = Math.floor((Date.now() - S.startTime) / 1000);
  const t = secs >= 60 ? `${Math.floor(secs/60)}m ${secs%60}s` : `${secs}s`;
  const txt = `I solved the Strands puzzle "${PUZZLE.theme}" in ${t} with ${S.hintsUsed} hint${S.hintsUsed!==1?'s':''}! 🎉\n${location.href}`;
  if (navigator.share) {
    navigator.share({ text: txt }).catch(()=>{});
  } else {
    navigator.clipboard.writeText(txt).then(() => {
      shareBtn.textContent = 'Copied!';
      setTimeout(() => { shareBtn.textContent = 'Share Result'; }, 2000);
    });
  }
});

// ── Confetti ──────────────────────────────────────────────────────────────────
function confetti() {
  const colors = ['#4a90e2','#e8a020','#e25555','#55c87a','#a855e2'];
  for (let i = 0; i < 50; i++) {
    const p = document.createElement('div');
    const size = 6 + Math.random() * 6;
    const left = Math.random() * 100;
    const delay = Math.random() * 0.6;
    const dur   = 1.5 + Math.random() * 1.5;
    const dx    = (Math.random() - 0.5) * 180;
    const rot   = Math.random() * 720;
    p.style.cssText = `
      position:fixed; width:${size}px; height:${size}px;
      border-radius:${Math.random()>0.5?'50%':'2px'};
      background:${colors[Math.floor(Math.random()*colors.length)]};
      left:${left}vw; top:-12px; z-index:200; pointer-events:none;
      animation: cf ${dur}s ${delay}s ease-in forwards;
    `;
    document.body.appendChild(p);
    setTimeout(() => p.remove(), (dur + delay + 0.1) * 1000);
  }
}
const cfStyle = document.createElement('style');
cfStyle.textContent = `@keyframes cf { to { top:110vh; opacity:0; transform:translateX(var(--dx,80px)) rotate(720deg); } }`;
document.head.appendChild(cfStyle);

// ── Util ──────────────────────────────────────────────────────────────────────
function cap(s) { return s.charAt(0) + s.slice(1).toLowerCase(); }

// ── Init ──────────────────────────────────────────────────────────────────────
refreshHintUI();
</script>
</body>
</html>"""


if __name__ == '__main__':
    main()
