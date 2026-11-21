#!/usr/bin/env python3
"""Polaris Acústica · user manual, Spanish and English (HTML pages rendered to PDF with Chrome).

  python3 tools/manual/build.py   ->  manual/PolarisAcustica-Manual-{ES,EN,EN-ES}.pdf

Needs: python playwright + Google Chrome, pypdf, and the fonts from npm:
  npm i @fontsource/space-grotesk @fontsource/inter @fontsource/jetbrains-mono   (in tools/manual, or set PA_FONTS)
The pictures are the app screenshots in docs/ (example data)."""
import os, pathlib, asyncio
from pypdf import PdfReader, PdfWriter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DOCS = ROOT / 'docs'
MAN = ROOT / 'manual'
FONTS = pathlib.Path(os.environ.get('PA_FONTS', HERE / 'node_modules' / '@fontsource'))
OUT = pathlib.Path('/tmp/pa_manual'); OUT.mkdir(exist_ok=True)

APP = 'https://drophlex.github.io/polaris-acustica/'
REPO = 'https://github.com/drophlex/polaris-acustica'
DON = 'https://www.paypal.com/donate?business=drophlex%40gmail.com&amp;currency_code=USD&amp;item_name=Polaris+Acustica'
IG, YT = 'https://www.instagram.com/polaris.sound.lab/', 'https://www.youtube.com/@PolarisSoundLab'
L = 'es'
def T(es, en): return en if L == 'en' else es

def font(fam, pkg, w, file=None):
    f = file or f'{pkg}-latin-{w}-normal.woff2'
    return f"@font-face{{font-family:{fam};font-weight:{w};src:url('file://{FONTS}/{pkg}/files/{f}')}}"
CSS = ''.join([font('SG', 'space-grotesk', w) for w in (500, 600, 700)] + [font('IN', 'inter', w) for w in (400, 500, 600)] +
              [font('JB', 'jetbrains-mono', w) for w in (400, 500)]) + """
@page{size:8.5in 11in;margin:0}*{box-sizing:border-box}
:root{--bg:#f2f4f7;--surface:#fff;--s2:#f7f8fa;--ink:#0f1b2d;--mute:#5b6779;--line:#dfe3ea;--accent:#2f54d6;--asoft:#e4eaff;
 --good:#12805a;--gsoft:#dcf3ea;--warn:#a86500;--wsoft:#fdeccc;--bad:#c23636;--bsoft:#fbe0e0}
html,body{margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font:10.1pt/1.5 IN,sans-serif;color:var(--ink);background:var(--bg)}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;padding:.56in .62in .8in;background:var(--bg)}
.page:last-child{page-break-after:auto}
a{color:var(--accent);text-decoration:none}
b{font-weight:600}
p{margin:0 0 .55em}
.kick{font:500 7.6pt/1 JB;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin-bottom:.1in;display:flex;gap:10px;align-items:center}
.kick:after{content:"";flex:1;height:1px;background:var(--line)}
h1{font:700 26pt/1.06 SG;letter-spacing:-.015em;margin:0 0 .12in}
h1 i{font-style:normal;color:var(--accent)}
h2{font:600 12.5pt/1.25 SG;margin:.16in 0 .06in}
h3{font:500 7.4pt/1.2 JB;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin:.12in 0 .05in}
.lead{font-size:11.4pt;line-height:1.5;color:#2b3a52}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:.13in .16in}
.card p{font-size:9.3pt;color:#33415a;margin:0}
.two{display:grid;grid-template-columns:1fr 1fr;gap:.2in;align-items:start}
.tw{display:grid;grid-template-columns:1.25fr 1fr;gap:.22in;align-items:start}
.wt{display:grid;grid-template-columns:1fr 1.3fr;gap:.22in;align-items:start}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.1in;margin:.08in 0 .12in}
figure{margin:0 0 .1in}
.shot{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 6px 18px rgba(15,27,45,.08)}
.shot img{display:block;width:100%}
figcaption{font-size:8.2pt;color:var(--mute);margin-top:5px}
table{width:100%;border-collapse:collapse;margin:.04in 0 .12in;font-size:9pt;background:var(--surface);border-radius:12px;overflow:hidden;border:1px solid var(--line)}
th{font:500 6.9pt JB;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);text-align:left;background:var(--s2);border-bottom:1px solid var(--line);padding:6px 8px}
td{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top}
tr:last-child td{border-bottom:0}
td:first-child{font-weight:600}
td.c{text-align:center;font-weight:500}
.steps{counter-reset:s;list-style:none;padding:0;margin:.06in 0 .12in}
.steps li{counter-increment:s;position:relative;padding:.05in 0 .07in .44in;border-bottom:1px solid var(--line);font-size:9.9pt}
.steps li:before{content:counter(s);position:absolute;left:0;top:.04in;width:.28in;height:.28in;border-radius:50%;background:var(--accent);color:#fff;font:600 10pt/.28in SG;text-align:center}
.note,.tip,.warn{border-radius:12px;padding:.09in .14in;margin:.08in 0 .12in;font-size:9.3pt}
.note{background:var(--asoft);color:#1d2f73}.tip{background:var(--gsoft);color:#0d4d37}.warn{background:var(--wsoft);color:#5c3a00}
.note b,.tip b,.warn b{font:500 7.2pt JB;letter-spacing:.14em;text-transform:uppercase;margin-right:6px}
.pill{display:inline-block;font:500 7.6pt/1 JB;padding:4px 8px;border-radius:99px;background:var(--asoft);color:var(--accent);margin:0 3px 4px 0}
.k{display:inline-block;font:500 8.2pt/1 IN;padding:3px 8px;border-radius:8px;background:var(--accent);color:#fff;vertical-align:1px}
.four{display:grid;grid-template-columns:repeat(4,1fr);gap:.08in;margin:.08in 0 .12in}
.four div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.09in .1in;font-size:8.6pt;color:#33415a}
.four div>b:first-child{display:block;font:500 7pt JB;letter-spacing:.14em;text-transform:uppercase;margin-bottom:3px}
.m{color:var(--accent)}.p{color:var(--bad)}.i{color:var(--good)}.s{color:var(--warn)}
.toc{display:grid;grid-template-columns:1fr 1fr;gap:2px 22px;font-size:9.4pt}
.toc div{display:flex;gap:10px;border-bottom:1px solid var(--line);padding:4px 0}
.toc span{font:500 8pt JB;color:var(--accent);width:20px}
.paypal{display:inline-block;font:600 8.4pt/1 SG;letter-spacing:.06em;color:#fff!important;background:#0070ba;border-radius:99px;padding:8px 16px 7px}
footer{position:absolute;left:.62in;right:.62in;bottom:.36in;display:flex;justify-content:space-between;font:500 6.8pt JB;letter-spacing:.16em;color:#8a95a7;text-transform:uppercase;border-top:1px solid var(--line);padding-top:7px}
.cover{background:radial-gradient(7in 5in at 100% 0%,#dfe6ff 0,transparent 60%),radial-gradient(6in 4in at 0% 100%,#e3f4ec 0,transparent 60%),var(--bg)}
.brand{display:flex;align-items:center;gap:12px;font:600 10pt/1.15 SG}
.brand img{width:44px;height:44px;border-radius:11px}
.ctitle{font:700 50pt/.95 SG;letter-spacing:-.03em;margin:.5in 0 .12in}
.ctitle i{font-style:normal;color:var(--accent)}
.csub{font:500 14pt/1.35 SG;color:#2b3a52;max-width:6in}
.ced{display:inline-block;margin-top:.18in;font:500 8pt JB;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);border-radius:99px;padding:6px 14px 5px}
.cshot{position:absolute;left:.62in;right:.62in;bottom:1.55in}
.cfoot{position:absolute;left:.62in;right:.62in;bottom:.42in;font-size:8.6pt;color:var(--mute);line-height:1.6}
"""

def shot(name, cap='', h=None, pos='top'):
    style = f' style="height:{h};object-fit:cover;object-position:{pos}"' if h else ''
    return f'<figure><div class="shot"><img src="file://{DOCS / name}"{style}></div>' + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>'
def table(head, rows, center=()):
    return '<table><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join(
        '<tr>' + ''.join(f'<td class="c">{c}</td>' if j in center else f'<td>{c}</td>' for j, c in enumerate(r)) + '</tr>' for r in rows) + '</table>'
def kick(t): return f'<div class="kick">{t}</div>'
def note(t, lab=None): return f'<div class="note"><b>{lab or T("Nota", "Note")}</b>{t}</div>'
def tip(t): return f'<div class="tip"><b>{T("Consejo", "Tip")}</b>{t}</div>'
def warn(t): return f'<div class="warn"><b>{T("Importante", "Important")}</b>{t}</div>'
def steps(items): return '<ol class="steps">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'

def pages():
    P = []
    # 1 · cover
    P.append(('cover', f'''<div class="brand"><img src="file://{ROOT / 'icons/icon-192.png'}"><div>POLARIS SOUND LAB<br><span style="color:var(--mute);font-weight:500">Mérida, Yucatán, México</span></div></div>
<div class="ctitle">Polaris<br><i>Acústica</i></div>
<div class="csub">{T('Mide el ruido y el eco de un espacio con tu teléfono y recibe un plan claro para que suene mejor.',
                    'Measure the noise and the echo of a room with your phone and get a clear plan to make it sound better.')}</div>
<div class="ced">{T('Manual de usuario · edición en español', 'User manual · English edition')}</div>
<div class="cshot">{shot('00-escritorio.png')}</div>
<div class="cfoot">{T('App web para iPhone, Android y computadora', 'Web app for iPhone, Android and computer')} · <a href="{APP}">drophlex.github.io/polaris-acustica</a><br>
Instagram <a href="{IG}">@polaris.sound.lab</a> · YouTube <a href="{YT}">@PolarisSoundLab</a> · {T('Las capturas usan datos de ejemplo.', 'Screenshots use example data.')}</div>'''))

    # 2 · what it is
    who = [(T('Trabajas o estudias en casa', 'You work or study at home'), T('entender por qué cuesta concentrarse o por qué en videollamadas te piden repetir', 'understand why it is hard to focus, or why people on video calls ask you to repeat')),
           (T('Sala de juntas u oficina', 'Meeting room or office'), T('saber si el cuarto rebota demasiado y cuánto material absorbente necesitas', 'know if the room is too echoey and how much absorbing material you need')),
           (T('Podcast, streaming, contenido', 'Podcast, streaming, content'), T('revisar tu cuarto de grabación antes de comprar equipo caro', 'check your recording room before buying expensive gear')),
           (T('Músico o profesor de música', 'Musician or music teacher'), T('mejorar el cuarto de ensayo o de clases', 'improve the rehearsal or lesson room')),
           (T('Docente', 'Teacher'), T('revisar si los alumnos del fondo entienden', 'check whether the students at the back can understand')),
           (T('Restaurante o local', 'Restaurant or venue'), T('detectar si el eco hace que todos tengan que gritar', 'find out if the echo makes everyone shout')),
           (T('Cine en casa', 'Home theater'), T('aclarar diálogos y controlar el rebote', 'clearer dialogue and less bounce')),
           (T('Duermes mal por ruido', 'Noise keeps you awake'), T('medir el fondo del dormitorio y ver qué sellar', 'measure the bedroom background and see what to seal')),
           (T('Instalador o técnico', 'Installer or technician'), T('una primera lectura rápida antes de una medición formal', 'a quick first reading before a formal measurement'))]
    toc = [T('Qué es y a quién le sirve', 'What it is and who it is for'), T('Tu primera medición', 'Your first measurement'), T('Leer el resultado', 'Reading the result'),
           T('El plan y la lista de compras', 'The plan and the shopping list'), T('Escucha la diferencia', 'Hear the difference'), T('Medidas avanzadas y modo Ingeniero', 'Advanced measurements and Engineer mode'),
           T('Calibrar el micrófono', 'Calibrating the microphone'), T('Gratis y Pro', 'Free and Pro'), T('Precisión, límites y privacidad', 'Accuracy, limits and privacy'), T('Preguntas frecuentes', 'FAQ')]
    P.append((T('Qué es', 'What it is'), f'''{kick(T('Qué es', 'What it is'))}<h1>{T('Tu cuarto, <i>explicado</i>', 'Your room, <i>explained</i>')}</h1>
<p class="lead">{T('Polaris Acústica escucha tu espacio durante menos de un minuto —un momento de silencio y un aplauso— y te dice en palabras sencillas:',
                   'Polaris Acústica listens to your room for less than a minute —a moment of silence and one clap— and tells you, in plain words:')}</p>
<div class="four"><div><b class="m">1</b>{T('cuánto <b>ruido de fondo</b> hay', 'how much <b>background noise</b> there is')}</div><div><b class="m">2</b>{T('cuánto <b>eco</b> (reverberación) tiene el cuarto', 'how much <b>echo</b> (reverberation) the room has')}</div>
<div><b class="m">3</b>{T('si eso es <b>adecuado para lo que haces ahí</b>', 'whether that is <b>right for what you do there</b>')}</div><div><b class="m">4</b>{T('<b>qué hacer, en qué orden y con qué materiales</b>', '<b>what to do, in what order and with which materials</b>')}</div></div>
<p>{T('Tiene dos modos: <b>Simple</b>, para quien no sabe de acústica, e <b>Ingeniero</b>, con curvas, bandas y métricas. Todo se calcula en tu dispositivo: el audio no se envía a ningún lado.',
      'It has two modes: <b>Simple</b>, for anyone who knows nothing about acoustics, and <b>Engineer</b>, with curves, bands and metrics. Everything is computed on your device: the audio is never sent anywhere.')}</p>
{'' if L == 'es' else note('The app itself is in Spanish. This manual shows its Spanish screens and gives every label in Spanish with its meaning in English.', 'Language')}
<h2>{T('¿A quién le sirve?', 'Who is it for?')}</h2>
{table([T('Si eres…', 'If you are…'), T('Te ayuda a…', 'It helps you…')], who)}
<h2>{T('Contenido', 'Contents')}</h2><div class="toc">{''.join(f'<div><span>{i + 1:02d}</span>{t}</div>' for i, t in enumerate(toc))}</div>'''))

    # 3 · first measurement
    P.append((T('Primera medición', 'First measurement'), f'''{kick(T('Tu primera medición · 5 minutos', 'Your first measurement · 5 minutes'))}<h1>{T('Silencio, <i>un aplauso</i> y listo', 'Silence, <i>one clap</i>, done')}</h1>
<div class="tw"><div>
<h3>{T('Abrir la app', 'Open the app')}</h3>
<p>{T('En el navegador de tu teléfono o computadora:', 'In the browser of your phone or computer:')} <a href="{APP}"><b>drophlex.github.io/polaris-acustica</b></a></p>
<p>{T('<b>Instálala como app:</b> en iPhone, Safari › Compartir › <i>Agregar a pantalla de inicio</i>. En Android, Chrome › menú › <i>Instalar app</i>. Después de abrirla una vez funciona sin internet.',
      '<b>Install it as an app:</b> on iPhone, Safari › Share › <i>Add to Home Screen</i>. On Android, Chrome › menu › <i>Install app</i>. After opening it once, it works offline.')}</p>
<h3>{T('Medir', 'Measure')}</h3>
{steps([T('Cuando pida permiso para el micrófono, pulsa <b>Permitir</b>.', 'When it asks for the microphone, tap <b>Allow</b> (<i>Permitir</i>).'),
        T('Entra al cuarto, cierra la puerta y ponte donde normalmente te sientas o hablas.', 'Go into the room, close the door and stand where you usually sit or talk.'),
        T('En <b>¿Para qué es el espacio?</b> elige el uso: dormitorio, sala, oficina, sala de juntas, aula, estudio o podcast, cine en casa, sala de música o restaurante. Cada uso tiene sus propios objetivos.',
          'In <b>¿Para qué es el espacio?</b> (what is the room for?) pick the use: bedroom, living room, office, meeting room, classroom, studio or podcast, home theater, music room or restaurant. Each use has its own targets.'),
        T('Opcional: escribe <b>largo, ancho y alto</b> en metros para calcular cuánto material necesitas.', 'Optional: type the <b>length, width and height</b> in meters, to work out how much material you need.'),
        T('Pulsa <span class="k">Empezar medición automática</span>. Quédate en silencio unos 15 segundos y, cuando la app lo indique, <b>da un aplauso fuerte</b>.',
          'Tap <span class="k">Empezar medición automática</span> (start automatic measurement). Stay silent for about 15 seconds and, when the app says so, <b>clap once, loud</b>.'),
        T('Lee el veredicto y el plan. Empieza por el primer paso: normalmente es lo más barato y lo que más ayuda.', 'Read the verdict and the plan. Start with step one: it is usually the cheapest and the one that helps most.'),
        T('Aplica el cambio, <b>vuelve a medir</b> y compara con la medición anterior.', 'Make the change, <b>measure again</b> and compare with the previous measurement.')])}
{tip(T('Si el aplauso sale débil o hay ruido, la app te lo dice: repite la medición.', 'If the clap is weak or the room is noisy, the app tells you: just measure again.'))}
</div><div>{shot('03-medir.png', T('Medir: el uso del espacio, sus medidas, el micrófono y la medición automática.', 'Measure: the room use, its size, the microphone and the automatic measurement.'), '6.9in')}</div></div>'''))

    # 4 · reading the result
    P.append((T('Leer el resultado', 'Reading the result'), f'''{kick(T('Leer el resultado', 'Reading the result'))}<h1>{T('Un veredicto <i>de 0 a 100</i>', 'A verdict <i>from 0 to 100</i>')}</h1>
<div class="wt"><div>{shot('01-resultado.png', T('Resultado en modo Simple.', 'Result in Simple mode.'), '6.3in')}</div><div>
<p>{T('Arriba ves la <b>puntuación</b> y el veredicto para el uso que elegiste (por ejemplo <i>Necesita atención</i>), con una frase que te dice qué hacer primero.',
      'At the top you see the <b>score</b> and the verdict for the use you picked (for example <i>Necesita atención</i>, needs attention), with one sentence telling you what to do first.')}</p>
<h3>{T('Las dos lecturas principales', 'The two main readings')}</h3>
{table([T('Lectura', 'Reading'), T('Qué te dice', 'What it tells you')],
       [(T('Ruido de fondo', 'Background noise'), T('El sonido que hay cuando "no hay nada": aire acondicionado, tráfico, zumbidos. En dB(A). La barra marca dónde estás y cuál es lo ideal para tu uso.',
                                                    'The sound there is when "nothing is on": air conditioning, traffic, hum. In dB(A). The bar shows where you are and what is ideal for your use.')),
        (T('Eco (reverberación)', 'Echo (reverberation)'), T('Cuánto tarda en apagarse un sonido, en segundos. La zona verde es el rango ideal.', 'How long a sound takes to die away, in seconds. The green zone is the ideal range.'))])}
<h3>{T('Las etiquetas', 'The labels')}</h3>
<p><span class="pill" style="background:var(--gsoft);color:var(--good)">{T('Bien · Aceptable', 'Good · Acceptable')}</span><span class="pill" style="background:var(--wsoft);color:var(--warn)">{T('Alto', 'High')}</span><span class="pill" style="background:var(--bsoft);color:var(--bad)">{T('Muy alto', 'Very high')}</span></p>
<h3>{T('Para darte una idea del ruido', 'To get a feel for noise')}</h3>
{table(['dB(A)', T('Se parece a…', 'Sounds like…')], [('30', T('dormitorio muy silencioso de noche', 'a very quiet bedroom at night')), ('40', T('oficina tranquila', 'a quiet office')),
       ('50', T('conversación suave', 'a soft conversation')), ('60', T('conversación normal', 'a normal conversation'))])}
<p style="font-size:9pt;color:var(--mute)">{T('Cada 10 dB más se oye como el doble de fuerte. Con 3 dB más ya se nota.', 'Every 10 dB more sounds about twice as loud. Just 3 dB more is already noticeable.')}</p>
{note(T('Si el micrófono no está calibrado, los decibelios llevan el aviso <i>Sin calibrar</i>. El eco y la claridad son confiables aun así.', 'If the microphone is not calibrated, the decibels carry a <i>Sin calibrar</i> (not calibrated) warning. Echo and clarity are reliable anyway.'))}
</div></div>'''))

    # 5 · plan + shopping list
    P.append((T('El plan', 'The plan'), f'''{kick(T('El plan y la lista de compras', 'The plan and the shopping list'))}<h1>{T('Qué hacer, <i>en qué orden</i>', 'What to do, <i>in what order</i>')}</h1>
<p class="lead">{T('El plan ordena las mejoras por impacto y costo. Cada paso se explica en cuatro partes:', 'The plan sorts the improvements by impact and cost. Every step is explained in four parts:')}</p>
<div class="four"><div><b class="m">{T('Medido', 'Measured')}</b>{T('lo que encontró la app', 'what the app found')}</div><div><b class="p">{T('Problema', 'Problem')}</b>{T('cómo se nota en tu día a día', 'how you notice it day to day')}</div>
<div><b class="i">{T('Lo ideal', 'Ideal')}</b>{T('a dónde hay que llegar para tu uso', 'where it should be for your use')}</div><div><b class="s">{T('Solución', 'Solution')}</b>{T('qué hacer y con qué', 'what to do and with what')}</div></div>
<div class="two"><div>{shot('02-plan.png', T('Tu plan: resultado esperado y pasos con su impacto y costo.', 'Your plan: expected result and steps with their impact and cost.'), '4.55in')}</div><div>
{shot('05-compras.png', T('Lista de compras con cantidades aproximadas.', 'Shopping list with approximate quantities.'), '2.45in')}
<p>{T('Toca la <b>i</b> de cada paso para ver por qué pasa, cómo hacerlo y cómo comprobarlo. Si escribiste las medidas del cuarto, el plan calcula el <b>resultado esperado</b> (por ejemplo, de 1.13 s a cerca de 0.50 s de eco) y la lista de compras trae cantidades.',
      'Tap the <b>i</b> on each step to see why it happens, how to do it and how to check it. If you typed the room size, the plan works out the <b>expected result</b> (for example, from 1.13 s to about 0.50 s of echo) and the shopping list has quantities.')}</p>
{tip(T('Empieza siempre por el paso 1 y vuelve a medir: muchas veces con sellar puertas o poner cortinas ya cambia mucho.', 'Always start with step 1 and measure again: sealing doors or hanging curtains often changes a lot already.'))}
</div></div>
<h2>{T('Problemas que resuelve', 'Problems it solves')}</h2>
{table([T('Lo que notas', 'What you notice'), T('Lo que mide', 'What it measures'), T('Lo que sugiere', 'What it suggests')],
       [(T('"Se oye como en una cueva"', '"It sounds like a cave"'), T('Eco por banda', 'Echo per band'), T('Cuántos paneles, cortinas o alfombra, y dónde', 'How many panels, curtains or rugs, and where')),
        (T('"Cuesta entender a quien habla"', '"Hard to understand speech"'), 'C50 · D50', T('Absorción en los primeros puntos de reflexión', 'Absorption at the first reflection points')),
        (T('"Retumban los graves"', '"The bass booms"'), T('Eco en graves', 'Low-frequency echo'), T('Trampas de esquina', 'Corner bass traps')),
        (T('"Hay un zumbido todo el día"', '"There is a hum all day"'), T('Espectro y tonos puros', 'Spectrum and pure tones'), T('Dónde buscar la fuente y cómo aislarla', 'Where to look for the source and how to isolate it')),
        (T('"Se oye lo de al lado"', '"I can hear next door"'), T('Aislamiento entre dos cuartos', 'Isolation between two rooms'), T('Sellado, masa y desacople', 'Sealing, mass and decoupling')),
        (T('"Tin-tin-tin al aplaudir"', '"Ping-ping-ping when clapping"'), T('Eco repetitivo', 'Flutter echo'), T('Absorber o romper el paralelismo', 'Absorb, or break the parallel walls'))])}'''))

    # 6 · hear the difference + advanced + engineer
    P.append((T('Escuchar y medir más', 'Listen and measure more'), f'''{kick(T('Escucha la diferencia · medidas avanzadas', 'Hear the difference · advanced measurements'))}<h1>{T('Oye el cambio <i>antes de comprar</i>', 'Hear the change <i>before you buy</i>')}</h1>
<div class="tw"><div>{shot('04-escucha.png', T('Escucha la diferencia.', 'Hear the difference (<i>Escucha la diferencia</i>).'))}</div><div>
<p>{T('Una voz de prueba pasa por el modelo de tu cuarto: <b>Seco</b> (sin cuarto), <b>Ahora</b> (como suena hoy) y <b>Después</b> (con el plan aplicado). También puedes <b>grabar tu voz 5 s</b> o <b>subir un audio</b>.',
      'A test voice goes through a model of your room: <b>Seco</b> (dry, no room), <b>Ahora</b> (now, how it sounds today) and <b>Después</b> (after, with the plan applied). You can also <b>record your voice for 5 s</b> or <b>upload audio</b>.')}</p>
{note(T('Es un modelo calculado con los tiempos de eco que mediste, no una grabación del cuarto. Sirve para darte una idea; se oye mejor con audífonos.', 'It is a model built from the echo times you measured, not a recording of the room. It gives you an idea; it sounds best on headphones.'))}
</div></div>
<h2>{T('Medidas avanzadas', 'Advanced measurements')}</h2>
<p>{T('En <b>Medidas avanzadas</b> puedes medir cada cosa por separado o con más precisión:', 'In <b>Medidas avanzadas</b> (advanced measurements) you can measure each thing separately or more precisely:')}</p>
{table([T('Medida', 'Measurement'), T('Para qué', 'What for')],
       [(T('Solo ruido', 'Noise only'), T('LAeq, LZeq, LA10/50/90, máximos y mínimos, espectro en tercios de octava y curva NC.', 'LAeq, LZeq, LA10/50/90, max and min, third-octave spectrum and NC curve.')),
        (T('Solo aplauso', 'Clap only'), T('El eco por bandas y la claridad sin repetir el silencio.', 'Echo per band and clarity without repeating the silence.')),
        (T('Barrido', 'Sweep'), T('La app toca un barrido de 6 s por la bocina y lo graba: más parejo que el aplauso. Usa una bocina externa: la del teléfono casi no da graves.', 'The app plays a 6 s sweep through the speaker and records it: smoother than a clap. Use an external speaker: a phone speaker has almost no bass.')),
        (T('Aislamiento entre dos cuartos', 'Isolation between two rooms'), T('Mide cuánto sonido pasa de un cuarto al otro, con el mismo micrófono.', 'Measures how much sound gets from one room into the other, with the same microphone.')),
        (T('Subir esa grabación', 'Upload a recording'), T('Analiza un audio que ya grabaste.', 'Analyses audio you already recorded.'))])}
<h2>{T('Micrófono', 'Microphone')}</h2>
<p>{T('Funciona con el micrófono del teléfono. Si conectas uno por <b>USB-C</b>, pulsa <b>Buscar micrófonos</b> y elígelo; el resultado dice con qué micrófono se midió.',
      'It works with the phone microphone. If you plug one in over <b>USB-C</b>, tap <b>Buscar micrófonos</b> (find microphones) and pick it; the result says which microphone was used.')}</p>'''))

    # 7 · engineer mode + glossary
    P.append((T('Modo Ingeniero', 'Engineer mode'), f'''{kick(T('Modo Ingeniero', 'Engineer mode'))}<h1>{T('Todas las <i>curvas y métricas</i>', 'Every <i>curve and metric</i>')}</h1>
<div class="wt"><div>{shot('07-ingeniero.png', T('Datos técnicos: niveles, espectro con curva NC y nivel en el tiempo.', 'Technical data: levels, spectrum with NC curve and level over time.'), '7.3in')}</div><div>
<p>{T('Cambia arriba de <b>Simple</b> a <b>Ingeniero</b> para ver los datos completos.', 'Switch at the top from <b>Simple</b> to <b>Ingeniero</b> (Engineer) to see all the data.')}</p>
{table([T('Término', 'Term'), T('Qué significa', 'What it means')],
       [('LAeq', T('Nivel promedio con ponderación A (como oye el oído).', 'Average level, A-weighted (as the ear hears).')),
        ('LZeq', T('Nivel promedio sin ponderar: incluye los graves.', 'Unweighted average level: includes the bass.')),
        ('LA10 · 50 · 90', T('Nivel superado el 10, 50 y 90 % del tiempo. LA90 es el fondo constante.', 'Level exceeded 10, 50 and 90 % of the time. LA90 is the steady background.')),
        ('NC', T('Curva de ruido: un número para comparar con el objetivo del uso (por ejemplo NC-30).', 'Noise criterion: one number to compare with the target for the use (e.g. NC-30).')),
        ('EDT', T('Caída inicial del eco: lo que el oído percibe primero.', 'Early decay time: what the ear notices first.')),
        ('T20 · T30', T('Tiempo de reverberación calculado con 20 o 30 dB de caída.', 'Reverberation time from a 20 or 30 dB decay.')),
        ('C50 · D50', T('Claridad de la voz. Más alto = se entiende mejor.', 'Speech clarity. Higher = easier to understand.')),
        (T('Modos de sala', 'Room modes'), T('Frecuencias graves que se acumulan por las medidas del cuarto.', 'Low frequencies that build up because of the room size.')),
        (T('Eco repetitivo', 'Flutter echo'), T('Rebote rápido entre paredes paralelas.', 'Fast bouncing between parallel walls.'))])}
<h3>{T('Exportar', 'Export')}</h3>
<p>{T('<b>Copiar informe</b> (texto) y <b>exportar CSV</b> con todos los datos. En Pro, <b>informe PDF</b> con tu nombre o empresa y logo.', '<b>Copy report</b> (text) and <b>export CSV</b> with all the data. In Pro, a <b>PDF report</b> with your name or company and logo.')}</p>
</div></div>'''))

    # 8 · calibration
    P.append((T('Calibración', 'Calibration'), f'''{kick(T('Calibrar el micrófono', 'Calibrating the microphone'))}<h1>{T('Cómo confiar en <i>los decibelios</i>', 'How to trust <i>the decibels</i>')}</h1>
<div class="tw"><div>
<p class="lead">{T('Un micrófono de teléfono no sabe cuántos decibelios mide. Sin calibrar, el nivel puede errar de ±5 a ±10 dB.', 'A phone microphone does not know how many decibels it hears. Uncalibrated, the level can be off by ±5 to ±10 dB.')}</p>
<h2>{T('La mejor forma', 'The best way')}</h2>
{steps([T('Pon un <b>sonómetro</b> junto al micrófono.', 'Put a <b>sound level meter</b> next to the microphone.'),
        T('Genera un ruido constante de 65 a 80 dB(A): un ventilador o ruido rosa.', 'Make a steady noise of 65 to 80 dB(A): a fan or pink noise.'),
        T('Mide 15 segundos con la app y anota la lectura <b>LAeq</b> del sonómetro.', 'Measure 15 seconds with the app and write down the meter\'s <b>LAeq</b> reading.'),
        T('En <b>Calibración del micrófono</b>, escribe esa lectura y pulsa <span class="k">Calibrar con la lectura</span>.', 'In <b>Calibración del micrófono</b>, type that reading and tap <span class="k">Calibrar con la lectura</span> (calibrate with the reading).')])}
<p>{T('Cada micrófono se calibra por separado y la calibración vale mientras no cambies su ganancia.', 'Each microphone is calibrated on its own, and the calibration holds as long as you do not change its gain.')}</p>
<h3>{T('Dependen de la calibración', 'Depend on calibration')}</h3>
<p>{T('El ruido en dB(A), la curva NC y la parte de ruido de la puntuación.', 'Noise in dB(A), the NC curve and the noise part of the score.')}</p>
<h3>{T('No dependen de la calibración', 'Do not depend on calibration')}</h3>
<p>{T('El tiempo de eco, la claridad (C50 y D50), los modos de sala y el aislamiento (con el mismo micrófono).', 'Echo time, clarity (C50 and D50), room modes and isolation (with the same microphone).')}</p>
{tip(T('¿No tienes sonómetro? Mide igual: el eco y la claridad ya son confiables, y para comparar antes y después basta con usar el mismo micrófono.', 'No meter? Measure anyway: echo and clarity are already reliable, and to compare before and after, just use the same microphone.'))}
</div><div>{shot('06-calibracion.png', T('El aviso de calibración en el resultado.', 'The calibration warning in the result.'), '6.6in')}</div></div>'''))

    # 9 · free and pro + dark mode
    rows = [(T('Medir ruido, eco, claridad y aislamiento', 'Measure noise, echo, clarity and isolation'), '✓', '✓'), (T('Veredicto y puntuación', 'Verdict and score'), '✓', '✓'),
            (T('Plan de mejora', 'Improvement plan'), T('3 primeros pasos', 'First 3 steps'), T('Completo', 'Complete')), (T('Lista de compras', 'Shopping list'), T('3 primeros artículos', 'First 3 items'), T('Completa', 'Complete')),
            (T('Escucha la diferencia y modo Ingeniero', 'Hear the difference and Engineer mode'), '✓', '✓'), (T('Copiar informe y exportar CSV', 'Copy report and export CSV'), T('✓ (informe con 3 pasos)', '✓ (report with 3 steps)'), T('✓ completo', '✓ complete')),
            (T('Proyectos guardados y comparar dos espacios', 'Saved projects and comparing two rooms'), '—', '✓'), (T('Informe PDF con tu nombre o empresa y logo', 'PDF report with your name or company and logo'), '—', '✓')]
    P.append((T('Gratis y Pro', 'Free and Pro'), f'''{kick(T('Gratis y Pro', 'Free and Pro'))}<h1>{T('Medir es <i>siempre gratis</i>', 'Measuring is <i>always free</i>')}</h1>
<p class="lead">{T('Medir es gratis y sin límite. Tu <b>primera medición real incluye todo Pro durante 24 horas</b> para que pruebes la herramienta completa. Después la app sigue funcionando, con estas diferencias:',
                   'Measuring is free and unlimited. Your <b>first real measurement includes all of Pro for 24 hours</b>, so you can try the full tool. After that the app keeps working, with these differences:')}</p>
{table(['', T('Gratis', 'Free'), T('Pro · 149 MXN, pago único', 'Pro · 149 MXN, one-time')], rows, center=(1, 2))}
<div class="two"><div class="card"><h3 style="margin-top:0">{T('Cómo se obtiene Pro', 'How to get Pro')}</h3>
<p>{T('Paga 149 MXN por PayPal desde la propia app y escríbeme: te envío tu <b>código personal</b>, normalmente el mismo día. Lo pegas en la app y funciona en cualquier dispositivo.',
      'Pay 149 MXN through PayPal from inside the app and write to me: I send you your <b>personal code</b>, usually the same day. Paste it in the app and it works on any device.')}</p></div>
<div class="card"><h3 style="margin-top:0">{T('¿Quieres que revise tu espacio?', 'Want me to look at your room?')}</h3>
<p>{T('Desde la app puedes enviarme tu informe por correo y platicamos qué conviene hacer. Es una orientación, no una medición profesional.', 'From the app you can email me your report and we talk about what to do. It is guidance, not a professional measurement.')}</p></div></div>
<h2>{T('Modo claro y oscuro', 'Light and dark mode')}</h2>
<div class="tw"><div><p>{T('La app sigue el modo de tu teléfono. El oscuro es cómodo para medir de noche, por ejemplo el ruido del dormitorio.', 'The app follows your phone\'s mode. Dark mode is comfortable for measuring at night, for example the bedroom noise.')}</p>
<h3>{T('Casos ideales', 'Best uses')}</h3>
<p>• {T('Primer diagnóstico <b>antes de gastar</b> en tratamiento acústico.', 'A first diagnosis <b>before spending</b> on acoustic treatment.')}<br>• {T('Comparar <b>antes y después</b> de una mejora: la app guarda la medición anterior.', 'Compare <b>before and after</b> an improvement: the app keeps the previous measurement.')}<br>
• {T('<b>Escuchar la diferencia</b> antes de comprar.', '<b>Hear the difference</b> before buying.')}<br>• {T('Explicarle a un cliente, compañero o familiar <b>por qué</b> hay que mejorar el espacio.', 'Show a client, colleague or family member <b>why</b> the room needs work.')}</p></div>
<div>{shot('08-oscuro.png', T('Modo oscuro.', 'Dark mode.'), '3.1in')}</div></div>'''))

    # 10 · limits, privacy, faq, contact
    faq = [(T('¿Necesito un micrófono especial?', 'Do I need a special microphone?'), T('No. Funciona con el del teléfono. Uno externo USB-C puede dar mejores resultados.', 'No. The phone\'s works. An external USB-C one can give better results.')),
           (T('¿Se graba o se sube mi audio?', 'Is my audio recorded or uploaded?'), T('No. Todo se procesa en tu dispositivo.', 'No. Everything is processed on your device.')),
           (T('¿Sustituye a un especialista?', 'Does it replace a specialist?'), T('No. Es una primera guía, no una medición certificada.', 'No. It is a first guide, not a certified measurement.')),
           (T('No me deja usar el micrófono.', 'It will not let me use the microphone.'), T('Revisa los permisos del navegador. El micrófono solo funciona en páginas con https.', 'Check the browser permissions. The microphone only works on https pages.')),
           (T('El aplauso no se detectó.', 'The clap was not detected.'), T('Aplaude más fuerte, más cerca del teléfono y con el cuarto en silencio; la app te avisa y puedes repetir.', 'Clap louder, closer to the phone, with the room quiet; the app tells you and you can repeat.'))]
    P.append((T('Límites y ayuda', 'Limits and help'), f'''{kick(T('Precisión, límites, privacidad y ayuda', 'Accuracy, limits, privacy and help'))}<h1>{T('Lo que <i>sí y no</i> puede hacer', 'What it <i>can and cannot</i> do')}</h1>
<div class="two"><div>
<h3>{T('Precisión y límites', 'Accuracy and limits')}</h3>
<p>• {T('Los decibelios dependen de la calibración. Sin calibrar son una estimación.', 'Decibels depend on calibration. Uncalibrated, they are an estimate.')}<br>
• {T('Los objetivos por uso y las curvas NC son orientativos y aún no se han verificado contra las normas.', 'The targets per use and the NC curves are guidance and have not yet been checked against the standards.')}<br>
• {T('No se ha validado contra un sonómetro certificado ni probado en todos los teléfonos. En iPhone el sistema puede procesar el audio del micrófono, y elegir micrófonos USB es más limitado que en Android.',
     'It has not been validated against a certified meter nor tested on every phone. On iPhone the system may process the microphone audio, and choosing USB microphones is more limited than on Android.')}<br>
• {T('La bocina de un teléfono casi no reproduce graves: para el barrido usa una bocina externa.', 'A phone speaker hardly plays bass: use an external speaker for the sweep.')}<br>
• {T('El plan es una guía, no un proyecto acústico.', 'The plan is a guide, not an acoustic design.')}</p>
{warn(T('Para certificaciones, normativas, contratos, conflictos legales, estudios profesionales o salas críticas, contrata una medición profesional con equipo certificado. Esta medición es orientativa y no la sustituye.',
        'For certifications, regulations, contracts, legal disputes, professional studios or critical rooms, hire a professional measurement with certified equipment. This measurement is guidance and does not replace it.'))}
<h3>{T('Privacidad', 'Privacy')}</h3>
<p>{T('Todo el análisis ocurre en tu dispositivo. El audio <b>no se envía a ningún servidor</b>. La página solo descarga las tipografías desde Google Fonts.', 'All the analysis happens on your device. The audio is <b>never sent to any server</b>. The page only downloads its fonts from Google Fonts.')}</p>
</div><div>
<h3>{T('Preguntas frecuentes', 'FAQ')}</h3>
{table([T('Pregunta', 'Question'), T('Respuesta', 'Answer')], faq)}
<div class="card"><h3 style="margin-top:0">{T('Sugerencias y contacto', 'Suggestions and contact')}</h3>
<p>{T('Las leo todas', 'I read them all')}: <b>drophlex@gmail.com</b><br>{T('Ideas para la app', 'Ideas for the app')}: <a href="{REPO}/issues/new/choose">{T('abre una propuesta en GitHub', 'open a proposal on GitHub')}</a><br>
{T('App', 'App')}: <a href="{APP}">drophlex.github.io/polaris-acustica</a></p>
<p style="margin-top:.1in">{T('Si te sirvió mi trabajo, invítame un café:', 'If my work helped you, buy me a coffee:')}</p><p style="margin-top:.06in"><a class="paypal" href="{DON}">♥ {T('DONAR CON PAYPAL', 'DONATE WITH PAYPAL')}</a></p></div>
<p style="font-size:8.6pt;color:var(--mute);margin-top:.14in">© 2026 Polaris Sound Lab · Mérida, Yucatán, México · <a href="{IG}">@polaris.sound.lab</a> · <a href="{YT}">YouTube @PolarisSoundLab</a></p>
</div></div>'''))
    return P

def render(lang, path):
    global L; L = lang
    body = []
    P = pages()
    for i, (title, html) in enumerate(P):
        if title == 'cover': body.append(f'<section class="page cover">{html}</section>'); continue
        body.append(f'<section class="page">{html}<footer><span>POLARIS ACÚSTICA · {T("MANUAL", "MANUAL")}</span><span>{title}</span><span>{i + 1:02d}</span></footer></section>')
    path.write_text(f'<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>{CSS}</style><body>{"".join(body)}</body></html>', encoding='utf-8')

async def to_pdf(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page()
        for src, out in jobs:
            await pg.goto('file://' + str(src)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
            over = await pg.evaluate("""[...document.querySelectorAll('.page')].map((pg, i) => { const r = pg.getBoundingClientRect(); let m = 0;
              pg.querySelectorAll('*').forEach(e => { if (e.closest('footer') || e.closest('.cfoot')) return; const q = e.getBoundingClientRect(); if (q.height) m = Math.max(m, q.bottom - r.top); });
              return [i + 1, Math.round(m)]; }).filter(x => x[1] > 990)""")
            await pg.pdf(path=str(out), width='8.5in', height='11in', print_background=True)
            print(out.name, 'overflow:', over)
        await b.close()

if __name__ == '__main__':
    MAN.mkdir(exist_ok=True)
    jobs = []
    for lang in ('es', 'en'):
        h = OUT / f'manual_{lang}.html'; render(lang, h); jobs.append((h, MAN / f'PolarisAcustica-Manual-{lang.upper()}.pdf'))
    asyncio.run(to_pdf(jobs))
    w = PdfWriter()
    for lang in ('en', 'es'):
        for p in PdfReader(str(MAN / f'PolarisAcustica-Manual-{lang.upper()}.pdf')).pages: w.add_page(p)
    with open(MAN / 'PolarisAcustica-Manual-EN-ES.pdf', 'wb') as f: w.write(f)
    print('PolarisAcustica-Manual-EN-ES.pdf', len(w.pages), 'pages')
