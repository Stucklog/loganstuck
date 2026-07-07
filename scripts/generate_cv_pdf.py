from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
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
    return [
        Spacer(1, 16),
        p(title.upper(), styles["SectionHeading"]),
        HRFlowable(width="100%", thickness=0.7, color=LINE, spaceBefore=5, spaceAfter=9),
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
        info.subject = "Public health evaluation, epidemiology, applied statistics, and data science CV"
        info.keywords = (
            "public health evaluation, monitoring and evaluation, MEL, epidemiology, "
            "statistics, biostatistics, data science, global health, R, program evaluation"
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
        subject="Public health evaluation, epidemiology, applied statistics, and data science CV",
        creator="ReportLab",
    )

    story = []
    story.append(p("Logan Stuck", styles["Name"]))
    story.append(p("Public Health Evaluation | Epidemiology | Applied Statistics | Data Science", styles["Headline"]))
    story.append(
        Paragraph(
            "Maasbommel, Netherlands | logan@loganstuck.com | "
            '<link href="https://loganstuck.com" color="#0e6f68">loganstuck.com</link>',
            styles["Contact"],
        )
    )
    story.append(
        p(
            "Public health evaluation and evidence specialist with expertise in epidemiology, "
            "monitoring and evaluation, statistical modeling, and data-informed decision support. "
            "Experience spans global health, academic research, consulting, and applied analytics, "
            "with collaborations across the United States, the Netherlands, Ethiopia, Ghana, South "
            "Africa, Tanzania, Uganda, Zanzibar, Zambia, and Zimbabwe.",
            styles["Body"],
        )
    )

    story.extend(section("Core skills", styles))
    story.append(
        p(
            "Program evaluation; monitoring, evaluation, and learning; epidemiology; biostatistics; "
            "causal inference; survival analysis; clinical trial simulation; predictive modeling; "
            "health economics; cost-effectiveness analysis; survey methodology; geospatial analysis; "
            "infectious disease surveillance; evidence synthesis; stakeholder reporting; R; SAS; "
            "STATA; QGIS; ArcGIS; ODK; Git; LaTeX.",
            styles["Body"],
        )
    )

    story.extend(section("Professional experience", styles))
    story.append(
        role(
            "2024 - Present",
            "Applied Statistician",
            "Biometris, Wageningen University and Research | Wageningen, Netherlands",
            [
                "Provide statistical consulting for internal research projects and industry collaborations.",
                "Conduct experimental design, data analysis, and predictive modeling across public health, environmental, and industry-related projects.",
                "Collaborate with researchers, policymakers, and industry partners to develop data-driven solutions.",
                "Translate complex analytical results into actionable insights and methodologically rigorous recommendations.",
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
                "Designed and conducted analyses for global health research projects, including clinical trials, individual participant data meta-analyses, and program evaluations.",
                "Applied causal inference, survival analysis, and statistical modeling to assess treatment effectiveness and disease burden.",
                "Led data-driven evaluations of tuberculosis diagnostics and infectious disease interventions.",
                "Led economic evaluations of tuberculosis health-care programs and mentored PhD and MSc students.",
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
                "Conducted malaria program evaluations to assess intervention effectiveness and disease transmission patterns.",
                "Led statistical analyses and epidemiological modeling to evaluate malaria surveillance and control strategies.",
                "Provided on-site training for household survey data collection, strengthening methodological rigor and data quality.",
                "Contributed to grant writing, scientific publications, and capacity-building initiatives in malaria research.",
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
                "Led evaluation of reactive case detection for malaria in Zanzibar, including effectiveness and cost-efficiency analyses.",
                "Synthesized evidence on diagnostic accuracy and geospatial prevalence mapping for malaria transmission patterns.",
                "Collaborated with local health authorities and global malaria programs to inform implementation strategy.",
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

    story.extend(section("Selected projects", styles))
    projects = [
        (
            "Data Science and Analytics Support for SHIFT2HEALTH",
            "2025 - Present | Wageningen University and Research",
            "Statistical and data science support for a multi-country project studying behavioral, physiological, and environmental contributors to obesity in shift workers.",
        ),
        (
            "Epidemiological Modeling and Trial Simulation for Rift Valley Fever Vaccine Development",
            "2024 - Present | LARISSA consortium",
            "Trial feasibility modeling, power simulations, and statistical methods guidance for Phase II and future vaccine evaluation.",
        ),
        (
            "Predictive Analytics for Amsterdam Quay Wall and Bridge Deterioration",
            "2024 - Present | City of Amsterdam",
            "Predictive modeling using spatio-temporal, geotechnical, laboratory, satellite, and structural monitoring data to support risk prioritization.",
        ),
        (
            "Multi-Country IPD Meta-Analysis on Subclinical Tuberculosis Prevalence",
            "2021 - 2024 | Amsterdam Institute for Global Health and Development",
            "Led data collection, harmonization, and design-adjusted analysis for a Lancet Infectious Diseases study of national tuberculosis prevalence surveys.",
        ),
        (
            "Assessment of the Zimbabwe Assistance Program in Malaria",
            "2019 - 2020 | Data for Impact and USAID",
            "Directed an evaluation integrating quantitative routine data analysis and qualitative research to inform malaria control strategy.",
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
                "City of Amsterdam, Modelling Deterioration of Amsterdam Quay Walls, 2024 - Present. Role: Primary analyst.",
                "Mr. Willem Bakhuys Roozeboomstichting, TBPS-Meta: Tuberculosis Prevalence Survey Meta Analyses, 2023. Role: Principal investigator.",
                "Amsterdam Tuberculosis Center, scTB-Meta: Subclinical Tuberculosis Meta Analyses, 2021 - 2023. Role: Principal investigator.",
                "EDCTP, CAGE-TB: Cough Audio Triage for Tuberculosis, 2022 - 2023. Role: Cost-effectiveness sub-study lead.",
                "EDCTP, PreFIT: Predicting the Future: Incipient Tuberculosis, 2021 - 2023. Role: Cost-effectiveness sub-study lead.",
                "EDCTP, TRiAD: Triage test for all oral DR TB regimen, 2020 - 2023. Role: Cost-effectiveness sub-study lead.",
                "Wellcome Trust, ROTA-biotic: Measuring the impact of rotavirus vaccines on paediatric antibiotic usage, 2020 - 2023. Role: Statistician.",
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
