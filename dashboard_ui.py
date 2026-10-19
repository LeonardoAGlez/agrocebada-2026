"""Presentation-only helpers. Scientific code and model contracts stay in src/agrocebada."""
from html import escape
import base64
from pathlib import Path
import streamlit as st

LEAF = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 48" fill="none" aria-hidden="true"><path d="M20 44V9M20 31C7 30 6 22 6 22C17 21 20 28 20 31ZM20 23C8 22 8 14 8 14C18 14 20 20 20 23ZM20 15C13 10 16 3 20 1C24 5 26 11 20 15ZM20 35C33 34 35 26 35 26C23 24 20 32 20 35ZM20 26C31 25 33 17 33 17C23 16 20 23 20 26Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'''


def style():
    st.html(Path(__file__).parent / 'ui_assets/dashboard.css')


def brand():
    leaf_src='data:image/svg+xml;base64,'+base64.b64encode(LEAF.replace('currentColor','#285947').encode()).decode()
    st.html(f'<div class="ac-brand"><img src="{leaf_src}" alt="" width="34" height="38"><div><strong>AgroCebada</strong><small>INTELIGENCIA DEL TERRITORIO</small></div></div>')


def hero(view, model_name):
    titles = {
        'Consultar parcelas': 'El campo, <em>en perspectiva.</em>',
        'Validación': 'Decisiones con <em>evidencia.</em>',
        'Fuentes': 'Cada dato tiene <em>una historia.</em>',
    }
    subtitle = {
        'Consultar parcelas': 'Explora el territorio, consulta cada parcela y descubre las estimaciones de rendimiento de la campaña 2025.',
        'Validación': 'Conoce cómo se evaluaron las estimaciones, sus errores y los límites de la investigación.',
        'Fuentes': 'Del satélite a la parcela: una mirada a los datos que sostienen esta investigación.',
    }
    art = '<svg class="ac-hero-art" viewBox="0 0 300 210" fill="none" aria-hidden="true">'
    for i in range(12):
        x=35+i*13
        art+=f'<path d="M{x} -10C{x-120} 75 {x+140} 110 {x+20} 230" stroke="#9cac8a" stroke-width=".7"/>'
    art+='</svg>'
    art_src='data:image/svg+xml;base64,'+base64.b64encode(art.replace('class="ac-hero-art"','xmlns="http://www.w3.org/2000/svg"').encode()).decode()
    art=f'<img class="ac-hero-art" src="{art_src}" alt="">'
    name = 'Ensamble R08' if model_name == 'selected' else 'Modelo del reto'
    st.html(f'''<div class="ac-topline"><span>OBSERVATORIO AGRÍCOLA / MÉXICO</span><span class="ac-status">{name} · Campaña 2025</span></div>
    <section class="ac-hero ac-motion">{art}<p class="ac-eyebrow">HIDALGO &nbsp; / &nbsp; TLAXCALA &nbsp; / &nbsp; PUEBLA</p>
    <h1>{titles[view]}</h1><p class="ac-subtitle">{subtitle[view]}</p></section>''')


def overview(master, metrics, model_name):
    scheme = 'CV estratificada · 5 grupos' if model_name == 'selected' else 'CV espacial · 5 grupos'
    cards = [
        ('Parcelas en estudio', str(len(master)), '', '138 observadas · 59 por predecir', False),
        ('Superficie del conjunto', f'{master.AREA_HA.sum():,.0f}', 'ha', 'Superficie de las 197 parcelas', False),
        ('Error absoluto medio', f'{metrics["mae"]:.3f}', 't/ha', scheme, True),
        ('RMSE de validación', f'{metrics["rmse"]:.3f}', 't/ha', scheme, False),
    ]
    markup='<div class="ac-stats ac-motion">'
    for label,value,unit,note,green in cards:
        markup+=f'<article class="ac-stat {"ac-green" if green else ""}"><span class="ac-stat-label">{label}</span><strong class="ac-stat-value">{value}</strong><span class="ac-stat-unit">{unit}</span><small class="ac-stat-note">{note}</small></article>'
    st.html(markup+'</div>')


def section(title, note=''):
    st.html(f'<div class="ac-section"><h2>{escape(title)}</h2><small>{escape(note)}</small></div>')


def distribution(master):
    markup='<div class="ac-side-bottom"><h4>Un territorio, tres estados.</h4>'
    for state,count in master.Estado.value_counts().items():
        markup+=f'<div class="ac-state"><span>{escape(state)}</span><b>{count} parcelas</b></div><div class="ac-bar"><i style="width:{100*count/len(master):.2f}%"></i></div>'
    st.html(markup+'</div>')


def chips(values):
    st.html(''.join(f'<span class="ac-chip">{escape(str(v))}</span>' for v in values))


def estimate_card(value, production):
    st.html(f'<div class="ac-estimate"><span>Estimación R08 · campaña 2025</span><strong>{value:.3f}<small>t/ha</small></strong><p>Producción estimada · {production:.2f} toneladas</p></div>')


def footer():
    st.html('<footer class="ac-footnote"><span>AGROCEBADA 2026 &nbsp; / &nbsp; Investigación aplicada al territorio</span><span>Estimaciones retrospectivas de 2025 · No valida campañas futuras</span></footer>')


def chart_theme(fig):
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font={'family':'Arial, sans-serif','color':'#748277','size':11},margin={'l':0,'r':12,'t':35,'b':18},legend={'orientation':'h','x':0,'y':1.13,'font':{'size':10}},hoverlabel={'bgcolor':'#ffffff','font_size':12})
    fig.update_xaxes(gridcolor='#edf1e8',zeroline=False)
    fig.update_yaxes(gridcolor='#edf1e8',zeroline=False)
    return fig
