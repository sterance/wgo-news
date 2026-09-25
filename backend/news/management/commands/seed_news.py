"""Fill the database with demo categories and articles.

    python manage.py seed_news

Safe to run repeatedly: existing categories and articles (matched by title)
are left alone. The articles are invented demo content, not real news.
"""

from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Category, News

CATEGORIES = [
    "nature", "war", "government", "politics", "education",
    "health", "economy", "business", "entertainment",
]


def expand_article(category, title, lead, context, reaction, outlook):
    p1 = (
        f"{lead} This development marks a pivotal moment for the {category} sector, as local communities, "
        f"industry experts, and administrative officials evaluate the immediate and wide-ranging ramifications. "
        f"Stakeholders across the region have noted that recent events have dramatically accelerated the need "
        f"for decisive intervention, elevating long-standing discussions into the forefront of public discourse. "
        f"As detailed reports continue to circulate, independent observers are closely tracking key operational "
        f"metrics to gauge both the immediate relief provided and the broader structural shifts taking place. "
        f"The initiative has drawn considerable interest from surrounding municipalities, with many looking to "
        f"this case as a potential benchmark for future policy frameworks and strategic resource allocation."
    )

    p2 = (
        f"{context} Historical analysis indicates that challenges of this magnitude rarely emerge in isolation; "
        f"rather, they stem from a complex interplay of systemic factors, regulatory evolutions, and shifting "
        f"environmental or socio-economic realities over extended periods. Over the past decade, domain specialists "
        f"have repeatedly highlighted how proactive planning, coupled with targeted infrastructure investments, "
        f"serves as a vital safeguard against unforeseen volatility. Without robust structural support and adaptive "
        f"governance, responding to these multi-faceted issues becomes increasingly difficult for administrative "
        f"bodies. Consequently, institutional leaders are placing renewed emphasis on empirical research and cross-sector "
        f"collaboration to build systemic resilience against future disruptions."
    )

    p3 = (
        f"{reaction} Industry analysts, civic advocates, and local representatives have expressed a diverse array "
        f"of perspectives regarding the implementation timeline and long-term priorities. 'We are observing an "
        f"unprecedented level of public engagement and institutional focus surrounding this matter,' stated a senior "
        f"policy strategist familiar with the ongoing developments. 'The primary hurdle now involves striking a "
        f"delicate balance between immediate emergency requirements and sustainable, long-term strategies that "
        f"deliver tangible benefits across all demographics.' Meanwhile, skeptical voices maintain that while initial "
        f"progress is encouraging, fundamental systemic reforms must be codified before lasting success can be claimed."
    )

    p4 = (
        f"{outlook} Moving forward, the coming months will prove decisive in assessing the durability and overall "
        f"efficacy of these measures as implementation phases advance. Comprehensive performance audits, alongside "
        f"ongoing public consultations, will be continuously monitored by oversight committees to ensure accountability "
        f"and operational transparency. As secondary initiatives begin to roll out, project leaders remain cautiously "
        f"confident that these combined efforts will establish a strong foundation for sustained progress, enhanced "
        f"safety, and long-term stability. Stakeholders across all affected sectors are scheduled to reconvene next "
        f"quarter to review updated data metrics and determine whether further legislative or administrative "
        f"adjustments are warranted."
    )

    return f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}"


# (pub_date, category, title, source, lead, context, reaction, outlook)
RAW_ARTICLES = [
    (
        timezone.make_aware(datetime(2026, 9, 24, 11, 13)),
        "nature",
        "Coastal town braces for a record-breaking king tide",
        "Demo Desk",
        "Residents of a low-lying coastal town are stacking sandbags and securing property this week as forecasters warn that the highest tidal surge in over a decade is due on Friday morning. Municipal council crews have closed foreshore car parks, deployed temporary high-capacity pump stations, and cleared storm drains.",
        "The impending tide stems from a rare astronomical alignment coinciding with a persistent low-pressure system off the coast. Oceanographers note that thermal expansion and strong onshore winds are adding thirty centimeters to baseline predictions, mirroring inundation patterns last seen eight years ago.",
        "Local business owners along the esplanade expressed deep concern over potential water damage and lost trading hours. 'While emergency sandbags help in the short term, we urgently need sea wall reinforcements,' noted the head of the local traders association during a emergency town hall meeting.",
        "Meteorologists expect water levels to peak early Friday before receding over the weekend. Secondary high tides on Saturday remain a risk, prompting authorities to keep emergency response units staged at vulnerable coastal access points.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 23, 14, 27)),
        "health",
        "Study links short daily walks to better sleep",
        "Demo Desk",
        "A comprehensive epidemiological study following two thousand adults over three years found that individuals who walked for at least twenty minutes daily fell asleep significantly faster and experienced fewer overnight awakenings. The findings highlight light physical activity as an accessible sleep intervention.",
        "Researchers monitored sleep architecture using wearable biometric sensors, correlating daily step counts with deep sleep duration. The data revealed consistent improvements across all age brackets, particularly among participants with high self-reported occupational stress levels.",
        "Sleep medicine specialists welcomed the publication, emphasizing that regular low-impact exercise helps calibrate circadian rhythms without causing central nervous system hyperarousal. Clinical psychologists noted that outdoor walks also offer valuable mental decompression time.",
        "Follow-up trials are currently being designed to evaluate whether morning walking yields superior circadian alignment compared to evening sessions. Public health organizations plan to integrate these findings into national sleep hygiene campaigns.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 22, 18, 41)),
        "economy",
        "Retail spending edges up as inflation cools",
        "Demo Wire",
        "Household retail expenditure registered a modest uptick last month as easing consumer price inflation provided shoppers with marginal relief in discretionary spending power. Official statistics released on Wednesday indicate steady gains in grocery, apparel, and hardware sectors.",
        "Financial analysts noted that while headline inflation has moderated over three consecutive quarters, elevated borrowing costs continue to constrain big-ticket household purchases like motor vehicles and furniture. Supply chain stabilization has helped keep supermarket shelf prices predictable.",
        "Retail trade groups described the figures as an encouraging sign of consumer stabilization ahead of the holiday season. 'Shoppers remain value-conscious, but willingness to spend on everyday discretionary items is returning,' commented a chief retail economist.",
        "Central bank officials will analyze retail turnover data during their upcoming interest rate review. Market observers anticipate that steady spending trends will support a holding pattern on monetary policy through the remainder of the fiscal quarter.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 21, 9, 53)),
        "education",
        "Universities trial shorter, more frequent assessments",
        "Demo Desk",
        "Three major regional universities are launching a joint pilot program next term to replace traditional high-stakes end-of-semester examinations with continuous, lower-weight academic assessments spread evenly across the teaching calendar.",
        "Educational researchers designed the assessment framework to reduce acute student anxiety and encourage continuous material engagement. Faculty departments spent several months restructuring course rubrics to accommodate weekly diagnostic quizzes and short practical projects.",
        "Student union representatives strongly endorsed the initiative, citing widespread exam burnout under current assessment models. Academic staff unions expressed cautious support while requesting monitoring of marking workloads for tutorial instructors.",
        "Institutional review boards will evaluate student retention rates, academic performance, and mental health metrics after two complete semesters. If successful, the continuous assessment model could be adopted institution-wide across participating campuses.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 20, 16, 9)),
        "government",
        "Parliament debates new digital privacy bill",
        "Demo Wire",
        "Federal lawmakers opened formal debate on Tuesday regarding a broad digital privacy reform bill aimed at imposing strict statutory limits on commercial data harvesting, consumer profiling, and automated decision-making systems.",
        "The proposed legislation updates decade-old data protection frameworks, introducing mandatory breach notifications, steep financial penalties for non-compliance, and an explicit right for citizens to request complete digital data erasure from commercial databases.",
        "Consumer privacy advocacy groups lauded the bill as a long-overdue safeguard against corporate overreach. Conversely, technology industry representatives warned that stringent compliance requirements could impose heavy operational burdens on emerging technology startups.",
        "Parliamentary committees are conducting clause-by-clause scrutiny of the draft bill over the next fortnight. A final vote in the lower house is scheduled before the parliamentary winter recess.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 19, 20, 34)),
        "entertainment",
        "Local film festival announces its biggest line-up yet",
        "Demo Desk",
        "Organizers of the city's annual independent film festival revealed an ambitious program featuring over one hundred feature films, documentaries, and short subjects, including twelve world premieres from emerging international directors.",
        "The festival expansion is supported by new municipal arts grants and venue partnerships across four cultural precincts. Highlights include a retro cinema retrospective and a dedicated outdoor family screening series hosted in the botanical gardens.",
        "Festival directors reported receiving record submission numbers from over fifty countries this season. 'The sheer quality and thematic diversity of independent cinema this year is unprecedented,' stated the chief festival programmer during the lineup launch.",
        "Advanced ticket sales open online next week, with box office analysts predicting sold-out screenings for several premiere titles. Industry networking sessions and filmmaking workshops will run concurrently throughout the fortnight.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 18, 13, 17)),
        "business",
        "Start-up unveils low-cost home battery",
        "Demo Wire",
        "A clean-tech startup based in Melbourne unveiled a modular residential energy storage battery engineered to retail at roughly one-third less than existing market models, utilizing an innovative cell architecture free of scarce cobalt.",
        "Engineers spent four years refining the battery's thermal management system and non-toxic iron-phosphate chemistry. The resulting units offer high charge-discharge efficiency, long lifecycle stability, and simple plug-and-play installation for solar-equipped homes.",
        "Energy market analysts highlighted the technology's potential to accelerate domestic solar self-consumption. 'Lowering hardware costs breaks down the major financial barrier for average households seeking energy independence,' noted a grid transition researcher.",
        "Commercial manufacturing lines are currently undergoing tooling upgrades, with initial customer deliveries scheduled for early next year. The company confirmed it has already logged thousands of advanced residential pre-orders.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 17, 10, 48)),
        "politics",
        "Leaders meet for talks on regional cooperation",
        "Demo Wire",
        "Senior political leaders and diplomatic delegations from across the regional bloc gathered in the capital on Monday for two days of bilateral talks focused on trade integration, renewable energy grid interconnectivity, and maritime security.",
        "The diplomatic summit comes amid shifting global economic alliances and shared climate challenges across regional sea lanes. Ministerial working groups spent weeks drafting joint policy accord frameworks prior to the summit opening.",
        "Foreign policy analysts observed that while alignment is strong on environmental protection, tariff negotiations remain complex. 'Sustaining open diplomatic dialogue is crucial for maintaining regional stability,' remarked a senior international relations fellow.",
        "Delegates are expected to issue a joint declaration at the summit conclusion outlining multilateral commitment milestones. Sub-committees will reconvene in six months to monitor implementation progress on agreed infrastructure projects.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 16, 7, 22)),
        "war",
        "Ceasefire monitors report a quiet weekend along the border",
        "Demo Desk",
        "International peacekeeping monitors reported a complete absence of military engagements or shellfire along the disputed border sector over the weekend, marking the longest period of sustained calm since the armistice was negotiated.",
        "Verification teams deployed satellite monitoring systems and ground patrols to confirm troop adherence to demilitarized buffer zone boundaries. Concurrently, civilian engineering crews began repairing damaged electrical grids along border townships.",
        "Humanitarian aid organizations seized the operational lull to dispatch medical supply convoys into previously isolated rural communities. 'Unhindered access allows us to deliver urgent medical care and food aid,' reported a field relief coordinator.",
        "Diplomatic mediators are utilizing the peaceful window to press both sides for formal talks on permanent border demarcation. Observer missions will maintain heightened surveillance along the buffer zone over the coming month.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 15, 15, 7)),
        "nature",
        "Forest managers test indigenous controlled burning techniques",
        "Demo Desk",
        "Forestry authorities teamed up with traditional land stewards to execute low-intensity cultural burns across thousands of hectares of dry forest, clearing combustible undergrowth while preserving canopy biodiversity ahead of summer.",
        "Cultural burning techniques utilize low-flame, slow-moving fire patterns that allow native fauna adequate time to retreat into unburned refuges. Ecological surveys confirm that soil nutrients and native seed banks remain intact post-burn.",
        "Environmental scientists commended the collaborative management approach, highlighting its superiority over heavy mechanical clearing. 'Integrating indigenous ecological knowledge creates far more resilient forest ecosystems,' observed a wildland fire researcher.",
        "Regional land management agencies plan to expand cultural burning workshops for rural volunteer fire brigades. Monitoring stations will track vegetation recovery and fauna return rates across the burn sites over the next two years.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 14, 12, 43)),
        "nature",
        "Rare migratory songbirds return to restored wetland reserve",
        "Demo Desk",
        "Ornithologists logged the return of endangered migratory songbird species to a coastal wetland reserve following a multi-year hydrological restoration project that re-established natural estuarine water flows.",
        "Civil engineers removed obsolete agricultural dikes and re-vegetated tidal mudflats with native sedges. The restored aquatic ecosystem rapidly regenerated invertebrate populations essential for migratory bird feeding stops.",
        "Conservation groups celebrated the bird sightings as conclusive proof of habitat recovery. 'Seeing breeding pairs nest in areas that were dry pasture five years ago is extraordinarily rewarding,' stated the reserve sanctuary director.",
        "Sanctuary management will enforce seasonal visitor buffer zones around key nesting sites throughout the breeding window. Water quality testing will continue monthly to ensure estuarine health remains optimal.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 13, 8, 19)),
        "nature",
        "Deep-sea expedition maps uncharted hydrothermal vent ecosystem",
        "Demo Wire",
        "Oceanographers aboard a deep-sea research vessel completed high-resolution bathymetric mapping of an underwater ridge, discovering previously unknown hydrothermal vent clusters supporting rich chemosynthetic marine life.",
        "Autonomous underwater vehicles equipped with stereoscopic cameras documented mineral chimneys venting mineral-laden water at extreme depths. Unique species of tubeworms, blind crabs, and specialized bacterial colonies were cataloged.",
        "Marine biologists highlighted the discovery's importance for understanding life in extreme environments. 'These vent fields are biological hotspots that provide critical insights into oceanic biodiversity,' explained the chief expedition scientist.",
        "Research teams plan to publish detailed genetic sequencing data of collected microbial specimens. Environmental groups are calling for international marine sanctuary status over the vent field to prevent deep-sea mining exploration.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 12, 17, 31)),
        "health",
        "Clinical trials show promise for dual-action migraine therapeutic",
        "Demo Desk",
        "Phase III clinical trials for a new oral therapeutic designed to simultaneously treat acute migraine attacks and prevent future onset yielded positive statistical results across primary safety and efficacy endpoints.",
        "The drug targets dual neuropeptide receptors involved in cranial neuro-inflammation and pain signaling pathways. Trial participants reported rapid pain relief within two hours alongside a dramatic decrease in monthly migraine frequency.",
        "Neurologists participating in the clinical study expressed optimism for patients who fail to respond to standard preventative treatments. 'Dual-action pharmaceuticals represent a major therapeutic leap in headache medicine,' noted a principal trial investigator.",
        "Pharmaceutical developers intend to submit full clinical trial dossiers to health regulators for marketing authorization early next year. Manufacturing facilities are being prepared for commercial-scale production upon regulatory clearance.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 11, 11, 56)),
        "health",
        "Regional health network launches mobile preventative care clinics",
        "Demo Desk",
        "A regional healthcare provider launched a fleet of mobile diagnostic vans outfitted with point-of-care testing equipment, digital imaging suites, and telehealth infrastructure to service remote agricultural townships.",
        "The mobile clinic initiative targets rural populations facing long travel distances to regional hospital centers. Services include routine cardiovascular checks, diabetic health monitoring, cancer screenings, and preventative health education.",
        "Rural community leaders warmly welcomed the mobile clinics, noting that early diagnostic access prevents severe health complications. 'Bringing healthcare directly to farm towns removes a major barrier for working families,' stated a local shire mayor.",
        "Operational managers will track patient intake metrics and diagnostic outcomes to refine mobile service schedules. Plans are underway to add specialized mobile dental units to the fleet before the end of the year.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 10, 14, 12)),
        "health",
        "Breakthrough research identifies microRNA markers for early Alzheimer's detection",
        "Demo Wire",
        "Molecular neuroscientists identified a distinct panel of circulating microRNA blood biomarkers capable of detecting pre-symptomatic neurodegenerative changes years before overt cognitive decline manifests.",
        "By analyzing longitudinal blood plasma samples from thousands of aging subjects, researchers isolated specific RNA signatures that correspond with early neuroinflammatory processes and synaptic degradation in the brain.",
        "Medical research institutes highlighted the diagnostic potential for early intervention therapeutic trials. 'Identifying neurodegeneration early allows disease-modifying therapies to be administered before irreversible damage occurs,' commented a lead neuroscientist.",
        "Independent pathology laboratories are initiating validation studies to standardize the microRNA blood test for routine clinical diagnostics. Pharmaceutical companies hope to utilize the biomarker assay in upcoming clinical drug trials.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 9, 16, 49)),
        "economy",
        "Central bank signals interest rate pause amidst stable employment data",
        "Demo Wire",
        "The monetary policy board voted to maintain the benchmark interest rate at its current setting, citing stable employment growth and gradual moderation in underlying inflation metrics.",
        "Latest economic indicators demonstrate sustained labor force participation alongside stabilizing wage growth figures. Central bank governors noted that prior interest rate adjustments are continuing to work through the financial system as intended.",
        "Financial market analysts viewed the decision as a sign of economic equilibrium. 'The central bank is balancing inflation control with economic growth, avoiding unnecessary drag on business investment,' noted a senior banking economist.",
        "Economic forecasting teams will evaluate upcoming quarterly consumer price indexes ahead of the next board meeting. Market expectations lean toward an extended interest rate pause through the remainder of the calendar year.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 8, 10, 24)),
        "economy",
        "Regional trade corridor expansion boosts agricultural export projections",
        "Demo Wire",
        "The completion of a modernized intermodal rail corridor connecting regional grain hubs with deep-water ocean ports is projected to boost agricultural export volumes by fifteen percent over the upcoming harvest season.",
        "The infrastructure upgrade includes automated grain handling terminals, expanded rail sidings, and upgraded bridge structures capable of accommodating heavier freight trains. Freight transit times to port terminals have been halved.",
        "Agricultural producer associations praised the transport project, highlighting significant reductions in freight logistics costs. 'Efficient freight links directly enhance our competitiveness in international grain markets,' stated a grain grower representative.",
        "Port authorities are upgrading grain storage silos to handle the anticipated surge in rail freight deliveries. Government transport departments are assessing secondary road upgrades to complement the primary rail corridor.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 7, 19, 8)),
        "economy",
        "Commercial real estate sector shifts toward energy-efficient retrofit projects",
        "Demo Desk",
        "Commercial property funds are reallocating capital from new high-rise developments toward energy efficiency retrofits of existing urban office towers to meet stringent municipal carbon emissions mandates.",
        "Retrofit projects involve installing smart building automation, double-glazed facade glass, heat pump HVAC systems, and rooftop solar arrays. Upgraded properties achieve substantial operational energy savings and elevated tenant occupancy.",
        "Real estate investment analysts noted that green building certifications now command premium leasing rates. 'Institutional tenants increasingly demand sustainable workplace facilities to meet corporate climate targets,' observed a property analyst.",
        "Municipal councils are offering expedited building permit approvals for deep energy retrofit projects. Industry bodies project that commercial retrofit expenditure will outpace new building construction over the coming decade.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 6, 9, 37)),
        "education",
        "State school district introduces nationwide digital literacy curriculum",
        "Demo Desk",
        "State education authorities introduced a mandatory digital literacy and cybersecurity curriculum across all public primary and secondary schools, focusing on media evaluation, AI ethics, and data privacy.",
        "The age-appropriate coursework was developed alongside child psychologists and technology specialists. Students learn to critically evaluate online information sources, identify synthetic media, and protect personal digital footprints.",
        "Parent-teacher associations expressed strong support for the educational update, noting the prevalence of online challenges facing youth. 'Teaching digital literacy is as fundamental today as teaching reading and mathematics,' remarked a school principal.",
        "Teacher training institutes are hosting professional development workshops to familiarize educators with the new curriculum modules. Annual student assessments will evaluate digital competency gains across participating school districts.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 5, 13, 51)),
        "education",
        "Apprenticeship programs see record enrollment following industrial subsidies",
        "Demo Wire",
        "Vocational training colleges reported unprecedented enrollment numbers across technical trade apprenticeships following the introduction of targeted government tuition fee subsidies and employer training incentives.",
        "Trade specializations experiencing the highest growth include electrical engineering, advanced manufacturing, and renewable energy system installation. Female enrollment in traditionally male-dominated trade courses grew by thirty percent.",
        "Trade union representatives praised the record uptake, pointing to chronic trade skill shortages across national construction projects. 'Investing in vocational education provides young people with high-paying, secure careers,' noted a union organizer.",
        "Vocational colleges are recruiting additional trade instructors and expanding workshop facilities to accommodate growing class sizes. Industry bodies are coordinating with colleges to ensure apprenticeship placements match regional labor demand.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 4, 15, 18)),
        "education",
        "Community colleges partner with tech firms for targeted workforce retraining",
        "Demo Desk",
        "A regional network of community colleges partnered with major software technology companies to offer intensive six-month certification programs designed to retrain mid-career workers for software development roles.",
        "The tuition-free curriculum covers cloud computing administration, data analytics, and software testing, combining asynchronous online modules with practical evening laboratory sessions mentored by industry professionals.",
        "Workforce development specialists highlighted the program's success in transitioning workers displaced by industrial automation into high-growth sectors. 'Accessible retraining pathways are vital for economic adaptability,' noted a workforce strategist.",
        "The initial cohort of graduates achieved high employment placement rates within local technology firms. Participating companies plan to double internship placements for the upcoming training intake.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 3, 11, 44)),
        "government",
        "National infrastructure authority approves high-speed rail corridor plan",
        "Demo Wire",
        "The national infrastructure advisory council granted formal alignment approval for a proposed high-speed passenger rail line connecting major metropolitan centers along the eastern industrial corridor.",
        "Environmental impact statements and engineering surveys confirmed the feasibility of electric tilt trains operating at speeds exceeding two hundred kilometers per hour, powered primarily by dedicated off-grid solar arrays.",
        "Transport planning experts hailed the corridor approval as a transformative step for regional connectivity. 'High-speed rail offers a fast, zero-emission alternative to domestic air travel between major cities,' noted a transport professor.",
        "Government finance ministers are reviewing public-private partnership models to fund track construction. Detailed engineering designs and land reservation orders will be finalized over the next eighteen months.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 2, 18, 29)),
        "government",
        "Municipal council introduces strict short-term rental compliance laws",
        "Demo Desk",
        "City council members voted unanimously to enact new compliance regulations for short-term holiday rentals, imposing annual booking night limits and mandatory property registration to address suburban housing availability.",
        "The municipal ordinance requires short-term accommodation hosts to hold public liability insurance and pay an annual registration fee. Automated monitoring software will cross-reference online listings to identify non-compliant properties.",
        "Housing advocacy organizations welcomed the local council action, citing acute long-term rental shortages for local residents. 'Returning short-term properties to the long-term rental pool alleviates housing stress,' argued a housing campaigner.",
        "Council enforcement officers will issue formal compliance notices to unregistered property owners starting next month. The municipal housing committee will review rental vacancy rates annually to assess policy effectiveness.",
    ),
    (
        timezone.make_aware(datetime(2026, 9, 1, 8, 52)),
        "government",
        "Maritime safety agency upgrades regional radar and automated beacon systems",
        "Demo Wire",
        "The national maritime safety authority completed a major technological upgrade of its coastal vessel tracking infrastructure, installing high-frequency radar units and automated oceanographic telemetry beacons along shipping channels.",
        "The upgraded sensor network provides coast guard control centers with real-time vessel position tracking, ocean current monitoring, and immediate collision avoidance alerts during adverse weather conditions.",
        "Commercial shipping pilot associations commended the navigation system upgrade. 'Enhanced radar clarity and real-time telemetry significantly reduce maritime risk across tight coastal straits,' commented a senior harbor pilot.",
        "Technicians will conduct monthly calibration tests across all newly installed coastal radar sites. Marine safety bulletins will incorporate real-time data feeds from the automated telemetry beacons.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 31, 14, 5)),
        "politics",
        "Bipartisan coalition drafts reform bill targeting campaign finance transparency",
        "Demo Wire",
        "A cross-party parliamentary coalition introduced draft legislation enforcing real-time public disclosure of political campaign donations and setting strict expenditure caps for political parties during election campaigns.",
        "The reform bill lowers mandatory donation disclosure thresholds from ten thousand dollars to five hundred dollars, requiring donations to be logged in a public online register within twenty-four hours of receipt.",
        "Electoral reform organizations strongly supported the bipartisan bill, describing transparency as essential for democratic integrity. 'Citizens deserve complete clarity regarding political financial backing,' stated a governance researcher.",
        "Parliamentary committees will hold public hearings on the draft bill across several capital cities. Reform proponents aim to pass the transparency legislation into law prior to the next general election cycle.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 30, 19, 39)),
        "politics",
        "City mayoral debate focuses on affordable housing zoning exemptions",
        "Demo Desk",
        "Candidates competing in the upcoming municipal mayoral election debated proposed zoning reform exemptions aimed at accelerating high-density affordable housing developments within established inner-city suburbs.",
        "The debate centered on balancing urban density requirements with heritage preservation and municipal parking infrastructure. Proposed policies include mandatory affordable housing allocations for major residential developments.",
        "Community turnout at the town hall debate was high, reflecting resident interest in urban planning decisions. 'Delivering affordable housing near transit corridors is the central challenge facing our city,' argued one mayoral candidate.",
        "Electoral polling indicates a close contest leading into election day. The elected council will vote on the proposed zoning reform amendments during its first official legislative session.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 29, 10, 16)),
        "politics",
        "Parliamentary committee opens public inquiry into regional electoral boundaries",
        "Demo Desk",
        "An independent electoral boundary commission launched a statutory public inquiry into regional electoral divisions following recent demographic shifts revealed by updated national census data.",
        "Census figures indicate significant population growth in outer-suburban growth corridors alongside population stagnation across certain rural inland districts, necessitating boundary adjustments to maintain equal voting representation.",
        "Political strategists from all major parties are reviewing proposed boundary maps. 'Ensuring fair demographic representation across electoral boundaries is a cornerstone of democratic voting systems,' noted an electoral analyst.",
        "The commission will conduct regional public hearings to gather community feedback on proposed division names and boundary lines. Final electoral boundary maps will be published at the conclusion of the inquiry.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 28, 16, 21)),
        "war",
        "Defense analysts evaluate cyber resilience measures along critical transport networks",
        "Demo Desk",
        "Defense policy analysts and cybersecurity specialists convened at a military symposium to evaluate system resilience across civilian air traffic control, port logistics, and freight rail signaling networks against cyber threats.",
        "The conference report highlighted an increasing frequency of automated network scanning targeting industrial control systems. Experts recommended adopting zero-trust software architectures and isolated hardware backup systems.",
        "Cybersecurity directors emphasized the necessity of public-private threat sharing partnerships. 'Protecting critical transportation infrastructure requires seamless coordination between military cyber units and civilian operators,' stated a panel speaker.",
        "Government defense agencies plan to issue updated cybersecurity standards for critical infrastructure operators next quarter. Joint cyber defense simulation exercises will be conducted annually.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 27, 7, 47)),
        "war",
        "Humanitarian corridor opens briefly to allow civilian evacuations from border sector",
        "Demo Wire",
        "A temporary local truce facilitated by international mediators permitted hundreds of civilians to safely evacuate a contested border sector through a designated demilitarized corridor monitored by Red Cross observers.",
        "Evacuation convoys transported vulnerable residents, families, and medical patients across checkpoints into receiving centers equipped with shelter and emergency medical teams.",
        "Relief agencies expressed relief over the successful evacuation while calling for extended humanitarian ceasefires. 'Safe civilian transit must be guaranteed by all parties under international law,' stressed a humanitarian mission chief.",
        "Diplomatic observers remain in contact with military commanders to negotiate further humanitarian windows. Relief organizations are stocking emergency supplies at border distribution centers.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 26, 12, 58)),
        "war",
        "Peacekeeping force deploys joint patrols to stabilize frontier agricultural zones",
        "Demo Desk",
        "Multinational peacekeeping contingents operating under a United Nations mandate initiated joint mobile patrols alongside local civil police to safeguard rural agricultural communities along volatile frontier zones.",
        "The patrol strategy focuses on securing key rural roads, agricultural markets, and water infrastructure during the seasonal grain harvest, preventing armed group incursions and protecting civilian livelihoods.",
        "Local community elders expressed gratitude for the heightened security presence along farm roads. 'Restoring security allows farmers to harvest crops without fear of armed harassment,' commented a local village leader.",
        "Peacekeeping commanders will maintain routine security patrols throughout the harvest period. Civilian affairs officers are conducting regular liaison meetings with community representatives to address local safety concerns.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 25, 15, 33)),
        "business",
        "Logistics giant shifts urban delivery fleet to hydrogen fuel cell vans",
        "Demo Wire",
        "A global freight logistics company announced plans to transition its entire inner-city parcel delivery fleet to heavy-duty hydrogen fuel cell vehicles over the next three years, establishing green hydrogen refueling hubs.",
        "The hydrogen fuel cell vehicles offer superior range and rapid refueling capabilities compared to battery-electric alternatives, maintaining operational uptime during high-volume delivery cycles.",
        "Transportation energy analysts praised the commercial investment in clean hydrogen technology. 'Decarbonizing commercial delivery fleets is crucial for reducing urban transport emissions,' noted a clean freight analyst.",
        "The logistics firm will commission its first solar-powered hydrogen refueling station next month. Initial vehicle fleet deployments will begin across central business district delivery routes.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 24, 9, 14)),
        "business",
        "Venture capital funding surges into agricultural biotech startups",
        "Demo Wire",
        "Private equity investment reports registered a sharp increase in venture capital funding allocated to early-stage agricultural biotechnology startups developing climate-resilient crop traits and biological soil inoculants.",
        "Funded technology platforms focus on crop genetics that withstand prolonged drought stress, biological nitrogen fixation to reduce synthetic fertilizer dependency, and automated indoor farming hardware.",
        "Agribusiness analysts attributed the investment surge to heightened global awareness of food security challenges. 'Biotechnology solutions offer scalable paths for sustainable agricultural production,' noted an agricultural investment director.",
        "Startups receiving capital infusions plan to expand field trial research across diverse climate zones. Regulatory advisory bodies are streamlining commercial evaluation processes for bio-based agricultural inputs.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 23, 17, 42)),
        "business",
        "Global manufacturing firm opens zero-waste semiconductor recycling facility",
        "Demo Desk",
        "An international electronics manufacturing enterprise commissioned a advanced closed-loop semiconductor recycling plant capable of recovering high-purity silicon and rare earth minerals from industrial electronic scrap.",
        "The recycling facility utilizes energy-efficient chemical extraction processes that consume significantly less electrical energy than primary mineral mining, preventing hazardous electronic waste accumulation in regional landfills.",
        "Environmental compliance authorities commended the circular manufacturing facility design. 'Recovering critical electronic minerals locally reduces supply chain vulnerability and environmental degradation,' stated an environmental manager.",
        "The plant will scale up recycling capacity over the next six months to process commercial e-waste from regional electronics assemblers. Recovered materials will be fed directly back into component manufacturing lines.",
    ),
    (
        timezone.make_aware(datetime(2026, 8, 22, 21, 4)),
        "entertainment",
        "Indie game studio wins international grand jury award for immersive narrative design",
        "Demo Desk",
        "A small independent video game studio operating from a regional tech hub captured the Grand Jury Prize at an international digital arts festival for its atmospheric narrative adventure title.",
        "The award-winning game was praised by jury members for its innovative interactive storytelling mechanics, hand-drawn art style, and original acoustic musical score recorded with a local youth orchestra.",
        "Video game industry commentators highlighted the recognition as a breakthrough moment for independent developers. 'Compelling storytelling and artistic vision continue to resonate globally,' noted a video game journalist.",
        "The development studio announced plans to release the game across major console platforms following the festival win. Studio founders intend to reinvest game profits into local digital arts mentoring programs.",
    ),
]


class Command(BaseCommand):
    help = "Create demo categories and news articles (idempotent)."

    def handle(self, *args, **options):
        categories = {}
        for name in CATEGORIES:
            categories[name], _ = Category.objects.get_or_create(name=name)

        created = 0
        for pub_date, category, title, source, lead, context, reaction, outlook in RAW_ARTICLES:
            content = expand_article(category, title, lead, context, reaction, outlook)
            _, was_created = News.objects.get_or_create(
                title=title,
                defaults={
                    "category": categories[category],
                    "source": source,
                    "content": content,
                    "date_and_time": pub_date,
                },
            )
            created += was_created

        self.stdout.write(self.style.SUCCESS(
            f"{len(CATEGORIES)} categories ready, {created} new article(s) added."
        ))