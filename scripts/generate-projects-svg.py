import json
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "project-data.json"
SVG_FILE = ROOT / "assets" / "featured-projects.svg"


def esc(value):
    return html.escape(str(value or ""))


def load_projects():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        projects = data.get("projects", [])
    else:
        projects = data

    return projects


def project_card(project, x, y, index):
    name = esc(project.get("name", "Unnamed Project"))
    description = esc(project.get("description", ""))
    technologies = project.get("technologies", [])
    status = esc(project.get("status", "Active"))
    github = project.get("github", "")
    live = project.get("live", "")

    if isinstance(technologies, list):
        tech = " • ".join(esc(item) for item in technologies)
    else:
        tech = esc(technologies)

    icon = {
        0: "RAM",
        1: "SEC",
        2: "WEB",
        3: "YT",
    }.get(index, "DEV")

    live_text = ""
    if live:
        live_text = f" • LIVE ↗"

    return f"""
    <a xlink:href="{esc(github)}" target="_blank">

      <g>

        <rect
          x="{x}"
          y="{y}"
          width="595"
          height="255"
          rx="4"
          fill="url(#panel)"
          stroke="#444444"/>

        <!-- HUD CORNERS -->

        <path
          d="M{x} {y+30}V{y}H{x+30}
             M{x+565} {y}H{x+595}V{y+30}
             M{x} {y+225}V{y+255}H{x+30}
             M{x+565} {y+255}H{x+595}V{y+225}"
          fill="none"
          stroke="#FFFFFF"
          stroke-width="2"/>


        <!-- PARTICLES -->

        <g
          clip-path="url(#card{index+1})"
          opacity=".5">

          <circle
            cx="{x+65}"
            cy="{y+65}"
            r="1.5"
            fill="#FFFFFF">

            <animate
              attributeName="cx"
              values="{x+45};{x+555};{x+45}"
              dur="{8 + index}s"
              repeatCount="indefinite"/>

          </circle>


          <circle
            cx="{x+390}"
            cy="{y+185}"
            r="1"
            fill="#FFFFFF">

            <animate
              attributeName="cy"
              values="{y+185};{y+35};{y+185}"
              dur="{6 + index}s"
              repeatCount="indefinite"/>

          </circle>


          <path
            d="M{x+35} {y+195}
               L{x+145} {y+105}
               L{x+270} {y+165}
               L{x+400} {y+55}
               L{x+565} {y+155}"
            fill="none"
            stroke="#FFFFFF"
            opacity=".16"
            stroke-dasharray="7 10">

            <animate
              attributeName="stroke-dashoffset"
              from="100"
              to="0"
              dur="{4 + index}s"
              repeatCount="indefinite"/>

          </path>

        </g>


        <!-- PROJECT ICON -->

        <rect
          x="{x+20}"
          y="{y+25}"
          width="55"
          height="55"
          fill="#0A0A0A"
          stroke="#777777"/>


        <text
          x="{x+47}"
          y="{y+61}"
          fill="#FFFFFF"
          font-family="monospace"
          font-size="14"
          text-anchor="middle">

          {icon}

        </text>


        <!-- PROJECT NAME -->

        <text
          x="{x+95}"
          y="{y+43}"
          fill="#FFFFFF"
          font-family="monospace"
          font-size="18"
          font-weight="700">

          {name}

          <animate
            attributeName="opacity"
            values="1;.55;1"
            dur="{4 + index * 0.4}s"
            repeatCount="indefinite"/>

        </text>


        <text
          x="{x+95}"
          y="{y+65}"
          fill="#777777"
          font-family="monospace"
          font-size="10">

          PROJECT MODULE // {index+1:02d}

        </text>


        <!-- STATUS -->

        <circle
          cx="{x+550}"
          cy="{y+36}"
          r="4"
          fill="#FFFFFF"
          filter="url(#glow)">

          <animate
            attributeName="opacity"
            values=".2;1;.2"
            dur="{1.2 + index * .2}s"
            repeatCount="indefinite"/>

        </circle>


        <text
          x="{x+540}"
          y="{y+61}"
          fill="#AAAAAA"
          font-family="monospace"
          font-size="9"
          text-anchor="end">

          {status.upper()}

        </text>


        <!-- DESCRIPTION -->

        <text
          x="{x+20}"
          y="{y+110}"
          fill="#AAAAAA"
          font-family="monospace"
          font-size="11">

          {description[:78]}

        </text>


        <!-- TECHNOLOGIES -->

        <text
          x="{x+20}"
          y="{y+145}"
          fill="#666666"
          font-family="monospace"
          font-size="9">

          STACK

        </text>


        <text
          x="{x+20}"
          y="{y+164}"
          fill="#FFFFFF"
          font-family="monospace"
          font-size="10">

          {tech[:82]}

        </text>


        <!-- TERMINAL -->

        <text
          x="{x+20}"
          y="{y+200}"
          fill="#777777"
          font-family="monospace"
          font-size="9">

          &gt; ./{name.upper().replace(" ", "_")[:35]} --status

        </text>


        <text
          x="{x+20}"
          y="{y+225}"
          fill="#FFFFFF"
          font-family="monospace"
          font-size="9">

          REPOSITORY: ONLINE

        </text>


        <text
          x="{x+575}"
          y="{y+225}"
          fill="#777777"
          font-family="monospace"
          font-size="9"
          text-anchor="end">

          GITHUB ↗{live_text}

        </text>

      </g>

    </a>
    """


def build_svg(projects):
    positions = [
        (35, 115),
        (670, 115),
        (35, 405),
        (670, 405),
    ]

    cards = []

    for index, project in enumerate(projects[:4]):
        x, y = positions[index]
        cards.append(
            project_card(project, x, y, index)
        )

    while len(cards) < 4:
        index = len(cards)
        x, y = positions[index]

        cards.append(
            f"""
            <rect
              x="{x}"
              y="{y}"
              width="595"
              height="255"
              rx="4"
              fill="url(#panel)"
              stroke="#222222"/>

            <text
              x="{x + 297}"
              y="{y + 130}"
              fill="#444444"
              font-family="monospace"
              font-size="12"
              text-anchor="middle">

              EMPTY PROJECT SLOT

            </text>
            """
        )

    return f"""<svg
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="1300"
height="720"
viewBox="0 0 1300 720">

<defs>

  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#000000"/>
    <stop offset="100%" stop-color="#0B0B0B"/>
  </linearGradient>

  <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#111111"/>
    <stop offset="100%" stop-color="#050505"/>
  </linearGradient>

  <pattern
    id="grid"
    width="40"
    height="40"
    patternUnits="userSpaceOnUse">

    <path
      d="M40 0H0V40"
      fill="none"
      stroke="#161616"
      stroke-width="1"/>

  </pattern>


  <filter id="glow">

    <feGaussianBlur
      stdDeviation="2"
      result="blur"/>

    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>

  </filter>


  <filter id="softGlow">

    <feGaussianBlur
      stdDeviation="5"
      result="blur"/>

    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>

  </filter>


  <clipPath id="card1">
    <rect x="35" y="115" width="595" height="255"/>
  </clipPath>

  <clipPath id="card2">
    <rect x="670" y="115" width="595" height="255"/>
  </clipPath>

  <clipPath id="card3">
    <rect x="35" y="405" width="595" height="255"/>
  </clipPath>

  <clipPath id="card4">
    <rect x="670" y="405" width="595" height="255"/>
  </clipPath>

</defs>


<!-- BACKGROUND -->

<rect
  width="1300"
  height="720"
  fill="url(#bg)"/>

<rect
  width="1300"
  height="720"
  fill="url(#grid)"/>


<!-- HEADER -->

<text
  x="45"
  y="55"
  fill="#FFFFFF"
  font-family="monospace"
  font-size="22"
  font-weight="700">

  // FEATURED_PROJECTS

</text>


<text
  x="1255"
  y="55"
  fill="#777777"
  font-family="monospace"
  font-size="11"
  text-anchor="end">

  PROJECT_MATRIX // 04 MODULES

</text>


<text
  x="45"
  y="80"
  fill="#AAAAAA"
  font-family="monospace"
  font-size="11">

  &gt; INITIALIZING PROJECT INTERFACE_

  <animate
    attributeName="opacity"
    values="1;.35;1"
    dur="1.2s"
    repeatCount="indefinite"/>

</text>


<circle
  cx="1248"
  cy="77"
  r="4"
  fill="#FFFFFF"
  filter="url(#glow)">

  <animate
    attributeName="opacity"
    values=".2;1;.2"
    dur="1.4s"
    repeatCount="indefinite"/>

</circle>


<text
  x="1238"
  y="81"
  fill="#BBBBBB"
  font-family="monospace"
  font-size="10"
  text-anchor="end">

  ONLINE

</text>


<line
  x1="40"
  y1="95"
  x2="1260"
  y2="95"
  stroke="#333333"/>


<!-- PROJECT CARDS -->

{"".join(cards)}


<!-- GLOBAL SCAN -->

<rect
  x="0"
  y="105"
  width="1300"
  height="2"
  fill="#FFFFFF"
  opacity=".12"
  filter="url(#softGlow)">

  <animate
    attributeName="y"
    values="105;665;105"
    dur="9s"
    repeatCount="indefinite"/>

</rect>


<!-- FOOTER -->

<text
  x="45"
  y="700"
  fill="#666666"
  font-family="monospace"
  font-size="10">

  &gt; PROJECT_MATRIX: OPERATIONAL

</text>


<text
  x="1255"
  y="700"
  fill="#666666"
  font-family="monospace"
  font-size="10"
  text-anchor="end">

  MUTHAIR_SYED // ENDPOINT_READY

</text>


</svg>
"""


def main():
    projects = load_projects()

    if not projects:
        raise RuntimeError(
            "No projects found in project-data.json"
        )

    SVG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    svg = build_svg(projects)

    SVG_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print(
        f"Generated {SVG_FILE} "
        f"using {min(len(projects), 4)} projects."
    )


if __name__ == "__main__":
    main()
