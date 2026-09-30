from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "docs" / "logan-stuck-cv.pdf"

INK = colors.HexColor("#12211f")
INK_SOFT = colors.HexColor("#2e4541")
PAPER = colors.HexColor("#f8f5ef")
TEAL = colors.HexColor("#0e6f68")
AMBER = colors.HexColor("#c47d2c")
LINE = colors.HexColor("#d8d6cf")


def p(text, style):
    return Paragraph(escape(text), style)


def linked(text, url, style):
    return Paragraph(f'<link href="{escape(url)}" color="#0e6f68">{escape(text)}</link>', style)


def bullet_list(items, styles):
    return [p(f"- {item}", styles["BulletText"]) for item in items]


def section(title, styles):
    rule = HRFlowable(width="100%", thickness=0.7, color=LINE, spaceBefore=5, spaceAfter=9)
    rule.keepWithNext = True
    return [
        CondPageBreak(130),
        Spacer(1, 16),
        p(title.upper(), styles["SectionHeading"]),
        rule,
    ]


def role(date, title, org, bullets, styles):
    return KeepTogether(
        [
            p(date, styles["Date"]),
            p(title, styles["RoleTitle"]),
            p(org, styles["Meta"]),
            Spacer(1, 4),
            *bullet_list(bullets, styles),
            Spacer(1, 9),
        ]
    )


def compact_entry(title, meta, description, styles):
    blocks = [p(title, styles["RoleTitle"])]
    if meta:
        blocks.append(p(meta, styles["Meta"]))
    if description:
        blocks.append(p(description, styles["Body"]))
    blocks.append(Spacer(1, 8))
    return KeepTogether(blocks)


def build_styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="Name",
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=34,
            textColor=INK,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            name="Headline",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=TEAL,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="Contact",
            fontName="Helvetica",
            fontSize=9.2,
            leading=13,
            textColor=INK_SOFT,
            alignment=TA_LEFT,
            spaceAfter=12,
        )
    )
    base.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=9.6,
            leading=13.2,
            textColor=INK_SOFT,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            name="BulletText",
            parent=base["Body"],
            leftIndent=10,
            firstLineIndent=-10,
            spaceAfter=3.2,
        )
    )
    base.add(
        ParagraphStyle(
            name="SectionHeading",
            fontName="Helvetica-Bold",
            fontSize=10.4,
            leading=12,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=0,
            keepWithNext=True,
        )
    )
    base.add(
        ParagraphStyle(
            name="RoleTitle",
            fontName="Helvetica-Bold",
            fontSize=10.8,
            leading=13.4,
            textColor=INK,
            spaceAfter=1,
        )
    )
    base.add(
        ParagraphStyle(
            name="Meta",
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.3,
            textColor=INK_SOFT,
            spaceAfter=3,
        )
    )
    base.add(
        ParagraphStyle(
            name="Date",
            fontName="Helvetica-Bold",
            fontSize=8.6,
            leading=10.5,
            textColor=AMBER,
            spaceAfter=2,
        )
    )
    return base


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, LETTER[1] - 0.18 * inch, LETTER[0], 0.18 * inch, fill=1, stroke=0)
    footer(canvas, doc)
    canvas.restoreState()


def later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)
    footer(canvas, doc)
    canvas.restoreState()


def footer(canvas, doc):
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK_SOFT)
    canvas.drawString(0.72 * inch, 0.44 * inch, "Logan Stuck | CV")
    canvas.drawRightString(LETTER[0] - 0.72 * inch, 0.44 * inch, f"Page {doc.page}")


def set_metadata(canvas, _doc):
    info = canvas._doc.info
    if isinstance(info, PDFInfo):
        info.title = "Logan Stuck - ATS-Friendly CV"
        info.author = "Logan Stuck"
        info.subject = "Public health evaluation, household surveys, epidemiology, and evidence-informed decision support CV"
        info.keywords = (
            "public health evaluation, household surveys, programme evaluation, monitoring and evaluation, "
            "MERL, epidemiology, biostatistics, GIS, global health, malaria, tuberculosis, R, ODK"
        )


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=LETTER,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.64 * inch,
        bottomMargin=0.68 * inch,
        title="Logan Stuck - ATS-Friendly CV",
        author="Logan Stuck",
        subject="Public health evaluation, household surveys, epidemiology, and evidence-informed decision support CV",
        creator="ReportLab",
    )

    story = []
    story.append(p("Logan Stuck", styles["Name"]))
    story.append(p("Public Health Evaluation and Evidence Specialist", styles["Headline"]))
    story.append(
        Paragraph(
            "Maasbommel, Netherlands | logan@loganstuck.com | "
            '<link href="https://loganstuck.com" color="#0e6f68">loganstuck.com</link><br/>'
            'Netherlands: <link href="tel:+31627377850" color="#0e6f68">+31 6 2737 7850</link> | '
            'United States: <link href="tel:+15042332873" color="#0e6f68">+1 504 233 2873</link>',
            styles["Contact"],
        )
    )
    story.append(
        p(
            "Public health evaluation and evidence specialist with expertise in epidemiology, "
            "household surveys, monitoring and evaluation, applied statistics, GIS, and evidence-informed "
            "decision support. PhD in epidemiology focused on malaria evaluation and elimination in "
            "Zanzibar, and a master's in biostatistics. More than one year of cumulative professional "
            "experience in sub-Saharan Africa, including living in Zanzibar. Works with research and "
            "implementation partners to translate findings for governments, NGOs, funders, and other "
            "decision-makers.",
            styles["Body"],
        )
    )
    story.append(
        p(
            "Focus: household-survey-based programme evaluation conducted with institutions and "
            "researchers in low- and middle-income countries. Interested in research and evaluation "
            "roles and independent consultancies spanning malaria, tuberculosis, and broader public "
            "health and international development.",
            styles["Body"],
        )
    )
    story.append(
        p(
            "Collaborations across the United States, the Netherlands, Ethiopia, Ghana, South Africa, "
            "Tanzania, Uganda, Zambia, and Zimbabwe.",
            styles["Body"],
        )
    )

    story.extend(section("Core skills", styles))
    story.append(
        p(
            "Evaluation: programme and intervention evaluation, mixed-methods evaluation, monitoring "
            "and evaluation, implementation research, evidence translation, stakeholder reporting. "
            "Surveys and fieldwork: study design, sampling, weighting, questionnaire development, "
            "digital data collection, field-team training, data-quality assurance. "
            "Analysis: epidemiology, biostatistics, complex survey analysis, GIS and spatial analysis, "
            "data visualisation, reproducible reporting, statistical modelling. "
            "Tools: R, R Markdown, Shiny, ggplot2, QGIS, ArcGIS, ODK, SAS, STATA, Git, LaTeX.",
            styles["Body"],
        )
    )

    story.extend(section("Professional experience", styles))
    story.append(
        role(
            "2024 - February 2027",
            "Applied Statistician",
            "Biometris, Wageningen University and Research | Wageningen, Netherlands",
            [
                "Provide statistical consulting for public health and applied research teams, including multi-country analytics for SHIFT2HEALTH.",
                "Design studies, analyses, and reproducible workflows that connect complex health data to practical decisions.",
                "Collaborate with researchers, policymakers, and implementation partners to align statistical methods with real-world evidence needs.",
                "Translate complex analytical results into clear recommendations, reports, and decision-ready outputs.",
            ],
            styles,
        )
    )
    story.append(
        role(
            "2020 - 2023",
            "Epidemiologist and Statistician",
            "Amsterdam Institute for Global Health and Development | Amsterdam, Netherlands",
            [
                "Led analyses for programme evaluations, national TB prevalence surveys, individual participant data meta-analyses, and clinical trials.",
                "Coordinated and harmonised national TB prevalence survey data with ministry and research partners across Africa and Asia, contributing to Lancet Infectious Diseases evidence.",
                "Applied complex survey methods, causal inference, survival analysis, and statistical modelling to assess infectious-disease burden and intervention performance.",
                "Mentored PhD and MSc students and translated complex findings for manuscripts, collaborators, and public health stakeholders.",
            ],
            styles,
        )
    )
    story.append(
        role(
            "2020 - 2023",
            "Lecturer in Statistics",
            "Vrije Universiteit Amsterdam | Amsterdam, Netherlands",
            [
                "Developed and taught epidemiology and statistics courses for Research Master's in Global Health students.",
                "Designed lectures, practical sessions, and workshops on biostatistics, causal inference, and data analysis.",
                "Created and graded assignments, exams, and research projects to assess statistical competencies.",
            ],
            styles,
        )
    )
    story.append(
        role(
            "2019 - 2020",
            "Postdoctoral Statistician, Epidemiologist, and Data Scientist",
            "Tulane University School of Public Health and Tropical Medicine | New Orleans, Louisiana",
            [
                "Conducted malaria programme evaluations assessing intervention effectiveness, transmission patterns, and surveillance performance.",
                "Led epidemiological and statistical analyses that informed malaria control and elimination strategies.",
                "Provided on-site training for household-survey data collection, strengthening data quality and field implementation.",
                "Contributed to peer-reviewed publications, grant development, and capacity-building initiatives in malaria research.",
            ],
            styles,
        )
    )
    story.append(
        role(
            "2015 - 2019",
            "Research Assistant",
            "Tulane University School of Public Health and Tropical Medicine | New Orleans, Louisiana",
            [
                "Led evaluation of reactive case detection for malaria in Zanzibar, from study design and field implementation to epidemiological and spatial analysis.",
                "Supported questionnaire development, field-team training, data-quality monitoring, and household-survey analysis for malaria intervention evaluations.",
                "Collaborated with health authorities and malaria programmes to translate findings into implementation strategy.",
            ],
            styles,
        )
    )
    story.append(
        role(
            "2013 - 2015",
            "Biostatistician Consultant",
            "HealthPartners Institute for Education and Research | Bloomington, Minnesota",
            [
                "Conducted power analyses and simulations for complex multicenter trials.",
                "Built randomization schedules, managed data, and conducted final analyses of trial data.",
                "Collaborated with principal investigators to interpret statistical findings accurately.",
            ],
            styles,
        )
    )

    story.extend(section("Selected evaluation and research projects", styles))
    projects = [
        (
            "Reactive Case Detection in Zanzibar",
            "2016 - 2019 | Tulane University",
            "Led study design, field implementation, and epidemiological and spatial analyses of malaria reactive case detection, translating findings with health authorities into options for elimination surveillance.",
        ),
        (
            "Tanzania School Net Programme",
            "2016 - 2019 | Tulane University",
            "Supported questionnaire development, field-team training, data-quality monitoring, and household-survey analysis to evaluate school-based distribution of insecticide-treated nets.",
        ),
        (
            "Ethiopia Malaria Indicator Survey",
            "2016 | Tulane University",
            "Led design-adjusted analysis of a national household survey, including weighting, malaria prevalence, intervention coverage, and geographic differences, contributing to the official report for health authorities and partners.",
        ),
        (
            "Zimbabwe Assistance Program in Malaria Assessment",
            "2019 - 2020 | Data for Impact and USAID",
            "Directed a mixed-methods evaluation combining routine programme data and qualitative research, with recommendations for PMI, USAID, and national malaria programme strategy.",
        ),
        (
            "Subclinical Tuberculosis IPD Meta-Analysis",
            "2021 - 2024 | Amsterdam Institute for Global Health and Development",
            "Led data coordination, harmonisation, and design-adjusted analysis across national TB prevalence surveys in Africa and Asia, working with ministry and research partners to produce policy-relevant evidence.",
        ),
        (
            "Trachoma Prevention Programme Evaluation",
            "2020 - 2021 | Tulane University and Sightsavers",
            "Analysed pre- and post-intervention surveys from more than 3,000 households and 100 schools in Malawi, Tanzania, and Uganda, translating findings into recommendations for hygiene and sanitation programmes.",
        ),
        (
            "BCG Vaccine Effectiveness IPD Meta-Analysis",
            "2022 - 2024 | Amsterdam Institute for Global Health and Development",
            "Provided methodological guidance on study design, data harmonisation, statistical modelling, interpretation, and manuscript development for a Lancet Microbe study.",
        ),
        (
            "SHIFT2HEALTH Analytics Support",
            "2025 - Present | Wageningen University and Research",
            "Statistical and data science support for a multi-country study of behavioural, physiological, nutritional, and environmental contributors to obesity in shift workers.",
        ),
        (
            "Rift Valley Fever Vaccine Trial Modelling",
            "2024 - Present | LARISSA consortium",
            "Epidemiological modelling, power calculations, and trial simulations for hRVFV-4s vaccine evaluation strategy.",
        ),
    ]
    for item in projects:
        story.append(compact_entry(*item, styles))

    story.extend(section("Education", styles))
    education = [
        ("PhD Epidemiology", "Tulane University School of Public Health and Tropical Medicine, 2015 - 2020", "Dissertation: An Evaluation of Reactive Case Detection for Malaria in Zanzibar."),
        ("MS Biostatistics", "University of Minnesota School of Public Health, 2010 - 2013", "Thesis: Spatial Quantification of Intra-Tumoral Heterogeneity."),
        ("BA Biology", "St. Olaf College, 2005 - 2009", ""),
    ]
    for item in education:
        story.append(compact_entry(*item, styles))

    story.extend(section("Teaching and capacity building", styles))
    story.append(
        KeepTogether(
            bullet_list(
            [
                "Co-Instructor, Nutrition and Infectious Disease, Health Sciences Master's, Vrije Universiteit Amsterdam, 2023.",
                "Lead Instructor, Introduction to Statistics, Research Master's in Global Health, Vrije Universiteit Amsterdam, 2021 - 2023.",
                "Co-Instructor, Intermediate Statistics and Epidemiology, Research Master's in Global Health, Vrije Universiteit Amsterdam, 2020 - 2023.",
                "Co-Instructor, Figure it Out, Applied Research, Research Master's in Global Health, Vrije Universiteit Amsterdam, 2020 - 2023.",
                "Guest Lecturer, Study Design in Quantitative Research, Department of Tropical Medicine, Tulane University School of Public Health and Tropical Medicine, 2020.",
                "Designed and led data analysis and GIS workshops for surveillance, monitoring, and evaluation officers in Tanzania and Zanzibar, 2019.",
                "Guest Lecturer, Surveillance in Malaria Elimination, Department of Tropical Medicine, Tulane University School of Public Health and Tropical Medicine, 2017.",
                "Co-promotor and methodological mentor for doctoral and master's students.",
            ],
            styles,
            )
        )
    )

    story.append(PageBreak())
    story.extend(section("Selected publications", styles))
    publications = [
        "Pelzer P.T., Stuck L., et al. Effectiveness of the primary Bacillus Calmette-Guerin vaccine against the risk of Mycobacterium tuberculosis infection and tuberculosis disease: a meta-analysis of individual participant data. The Lancet Microbe, 2025.",
        "Stuck L., Klinkenberg E., et al. Prevalence of subclinical pulmonary tuberculosis in adults in community settings: an individual participant data meta-analysis. The Lancet Infectious Diseases, 2024.",
        "Das A.M., Hetzel M.W., Yukich J.O., Stuck L., et al. Modelling the impact of interventions on imported, introduced and indigenous malaria infections in Zanzibar, Tanzania. Nature Communications, 2023.",
        "Stuck L., van Haaster A.C., Kapata-Chanda P., Klinkenberg E., Kapata N., Cobelens F. How subclinical is subclinical tuberculosis? An analysis of national prevalence survey data from Zambia. Clinical Infectious Diseases, 2022.",
        "Stuck L., et al. Malaria infection prevalence and sensitivity of reactive case detection in Zanzibar. International Journal of Infectious Diseases, 2020.",
        "Stuck L., Lutambi A., Chacky F., et al. Can school-based distribution be used to maintain coverage of long-lasting insecticide treated bed nets? Health Policy and Planning, 2017.",
    ]
    story.extend(bullet_list(publications, styles))

    story.extend(section("Grants, contracts, and consultancies", styles))
    story.append(
        KeepTogether(
            bullet_list(
            [
                "CEPI, LARISSA II: Novel Rift Valley Fever Vaccine Development, 2024 - Present. Role: Trial feasibility modeller.",
                "Mr. Willem Bakhuys Roozeboomstichting, TBPS-Meta: Tuberculosis Prevalence Survey Meta Analyses, 2023. Role: Principal investigator.",
                "Amsterdam Tuberculosis Center, scTB-Meta: Subclinical Tuberculosis Meta Analyses, 2021 - 2023. Role: Principal investigator.",
                "USAID, Associate Award: Technical assistance and support for community-based malaria surveillance in Tanzania, 2017 - 2019. Role: Co-investigator for sub-study.",
                "PATH / MACEPA / Gates Foundation, technical and scientific support to MACEPA activities in Zambia, 2017 - 2019. Role: Analytic and field support.",
                "USAID, VectorWorks, 2016 - 2019. Role: Analytic and field support.",
                "Data for Impact, Assessment of the Zimbabwe Assistance Program in Malaria, 2019 - 2020. Role: Evaluation consultant.",
                "Sightsavers, Schistosomiasis and Helminthiasis School Survey in Guinea-Bissau, 2018. Role: Consultant.",
                "Sightsavers, Multi-country WASH intervention trial in sub-Saharan Africa, 2017 - 2018. Role: Consultant.",
            ],
            styles,
            )
        )
    )

    def first(canvas, doc_obj):
        set_metadata(canvas, doc_obj)
        first_page(canvas, doc_obj)

    def later(canvas, doc_obj):
        set_metadata(canvas, doc_obj)
        later_pages(canvas, doc_obj)

    doc.build(story, onFirstPage=first, onLaterPages=later)
    return OUT


if __name__ == "__main__":
    print(build_pdf())
