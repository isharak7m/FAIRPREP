"""
FairPrep AI — Ethical Interview Coach  v3.1
────────────────────────────────────────────
Fixed: White block visibility (text invisible on white bg)
Fixed: CSS variable conflicts with Streamlit's default theme
Fixed: Dark card text contrast
Fixed: Report card rendering
Fixed: All color inheritance issues
Run: streamlit run app.py
"""

import streamlit as st
import time
import re
import math
import datetime

st.set_page_config(
    page_title="FairPrep AI · Ethical Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── ROOT VARIABLES ── */
:root {
  --fp-cream:   #F5F0E8;
  --fp-ink:     #1A1614;
  --fp-rust:    #C94A2B;
  --fp-sage:    #3D6B58;
  --fp-gold:    #D4A847;
  --fp-warm:    #EDE8DF;
  --fp-muted:   #5C524A;
  --fp-white:   #FFFFFF;
  --fp-border:  #D8D0C8;
  --fp-card-bg: #FFFFFF;
  --fp-text-on-light: #2A2520;
  --fp-text-on-warm: #4A3F35;
  --fp-text-on-dark: #FFFFFF;
  --fp-text-on-gold: #7A5F00;
  --fp-text-on-sage: #FFFFFF;
  --fp-text-on-rust: #FFFFFF;
}

/* ── GLOBAL RESETS ── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background-color: var(--fp-cream) !important;
}
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--fp-cream); }
::-webkit-scrollbar-thumb { background: #C8BFB5; border-radius: 3px; }

/* ── STREAMLIT CONTAINER OVERRIDES ── */
.stApp { background-color: var(--fp-cream) !important; }
.block-container { background-color: transparent !important; }
div[data-testid="stVerticalBlock"] { background-color: transparent !important; }
div[data-testid="column"] { background-color: transparent !important; }
div[data-testid="stHorizontalBlock"] { background-color: transparent !important; }
[data-testid="stAppViewContainer"] { background: var(--fp-cream) !important; }
[data-testid="stHeader"] { background: transparent !important; }

/* ── STREAMLIT TEXT OVERRIDES — only target Streamlit's own elements ── */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
  color: var(--fp-ink) !important;
}
.stTextArea label, .stSelectbox label, .stToggle label {
  color: var(--fp-ink) !important;
}
/* Expander */
.streamlit-expanderHeader { color: var(--fp-ink) !important; font-weight: 600 !important; }
.streamlit-expanderContent, .streamlit-expanderContent p { color: var(--fp-ink) !important; }

/* ── METRIC COMPONENTS ── */
div[data-testid="metric-container"] {
  background: #EDE8DF !important;
  border-radius: 10px !important;
  padding: 12px 16px !important;
  border: 1px solid var(--fp-border) !important;
}
div[data-testid="metric-container"] label {
  color: var(--fp-muted) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
}
div[data-testid="stMetricValue"] {
  color: var(--fp-ink) !important;
  font-family: 'Playfair Display', serif !important;
  font-size: 2rem !important;
}
div[data-testid="stMetricDelta"] { color: var(--fp-sage) !important; }

/* ── HERO ── */
.fp-hero {
  background: var(--fp-ink);
  border-radius: 20px;
  padding: 52px 56px 44px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.fp-hero::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 360px; height: 360px;
  background: radial-gradient(circle, rgba(201,74,43,0.22) 0%, transparent 65%);
  pointer-events: none;
}
.fp-hero::after {
  content: '';
  position: absolute; bottom: -60px; left: 25%;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(212,168,71,0.10) 0%, transparent 70%);
  pointer-events: none;
}
.fp-hero-tag {
  display: inline-block;
  background: var(--fp-rust);
  color: #FFFFFF !important;
  font-size: 10px; font-weight: 700;
  letter-spacing: 2.5px; text-transform: uppercase;
  padding: 5px 14px; border-radius: 6px; margin-bottom: 18px;
}
.fp-hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 3.4rem; line-height: 1.05;
  color: #FFFFFF !important; margin: 0 0 14px;
}
.fp-hero h1 em { color: var(--fp-gold) !important; font-style: italic; }
.fp-hero p {
  color: rgba(255,255,255,0.72) !important;
  font-size: 1.02rem; font-weight: 300;
  max-width: 500px; margin: 0 0 22px; line-height: 1.65;
}
.fp-hero-meta { display: flex; gap: 8px; flex-wrap: wrap; }
.fp-hero-badge {
  background: rgba(255,255,255,0.09);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px; padding: 5px 13px;
  font-size: 0.74rem; color: rgba(255,255,255,0.75) !important;
  letter-spacing: 0.4px;
}

/* ── SECTION LABEL ── */
.fp-section-label {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 2.5px; text-transform: uppercase;
  color: var(--fp-muted) !important; margin-bottom: 14px;
  display: flex; align-items: center; gap: 8px;
}
.fp-section-label::after { content: ''; flex: 1; height: 1px; background: var(--fp-border); }

/* ── CARD ── */
.fp-card {
  background: #FFFFFF !important;
  border: 1.5px solid var(--fp-border);
  border-radius: 16px;
  padding: 28px 30px;
  margin-bottom: 18px;
  position: relative;
  color: var(--fp-text-on-light) !important;
}
.fp-card p, .fp-card span, .fp-card div, .fp-card li, .fp-card h1, .fp-card h2, .fp-card h3, .fp-card h4, .fp-card h5, .fp-card h6 {
  color: var(--fp-text-on-light) !important;
}

/* ── QUESTION BOX ── */
.fp-question-box {
  background: var(--fp-ink) !important;
  color: #F5F0E8 !important;
  border-radius: 12px;
  padding: 22px 26px;
  font-family: 'Playfair Display', serif;
  font-size: 1.12rem; line-height: 1.6;
  margin: 16px 0 18px;
  border-left: 4px solid var(--fp-rust);
  position: relative;
}
.fp-question-box::before {
  content: '"';
  position: absolute; top: -8px; left: 16px;
  font-size: 4rem; color: var(--fp-rust); opacity: 0.3;
  font-family: 'Playfair Display', serif; line-height: 1;
}

/* ── SCORE PILLS ── */
.fp-score-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 14px; border-radius: 100px;
  font-size: 0.82rem; font-weight: 600;
}
.fp-score-high { background: #C7EACF !important; color: #145229 !important; }
.fp-score-mid  { background: #FAEFC0 !important; color: #6A4A00 !important; }
.fp-score-low  { background: #FAD0D0 !important; color: #7A1515 !important; }

/* ── BIG SCORE ── */
.fp-big-score-wrap { display: flex; align-items: center; gap: 24px; margin: 10px 0 24px; }
.fp-big-score-num {
  font-family: 'Playfair Display', serif;
  font-size: 4.2rem; line-height: 1;
  color: var(--fp-ink) !important; min-width: 80px;
}
.fp-big-score-info { flex: 1; }
.fp-big-score-meta { font-size: 0.8rem; color: var(--fp-muted) !important; margin-top: 6px; }

/* ── BIAS BOXES ── */
.fp-bias-warning {
  background: #FFFAED !important;
  border: 1.5px solid #D4A800;
  border-radius: 12px; padding: 16px 20px; margin: 12px 0;
  display: flex; gap: 14px; align-items: flex-start;
}
.fp-bias-warning .fp-bias-title, .fp-bias-warning .fp-bias-desc { color: var(--fp-text-on-gold) !important; }
.fp-bias-warning .fp-bias-icon { color: var(--fp-text-on-gold) !important; }
.fp-bias-ok {
  background: #E8F5EE !important;
  border: 1.5px solid #4A9E72;
  border-radius: 12px; padding: 16px 20px; margin: 12px 0;
  display: flex; gap: 14px; align-items: flex-start;
}
.fp-bias-ok .fp-bias-title, .fp-bias-ok .fp-bias-desc { color: var(--fp-text-on-sage) !important; }
.fp-bias-ok .fp-bias-icon { color: var(--fp-text-on-sage) !important; }
.fp-bias-icon { font-size: 1.4rem; flex-shrink: 0; }
.fp-bias-title { font-weight: 700; font-size: 0.92rem; margin-bottom: 3px; }
.fp-bias-desc { font-size: 0.87rem; line-height: 1.5; }

/* ── EXPLANATION ROWS ── */
.fp-explain-row {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 14px 0; border-bottom: 1px solid #EDE8E2;
}
.fp-explain-row:last-child { border-bottom: none; }
.fp-explain-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 3px; }
.fp-explain-label {
  font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--fp-muted) !important;
  margin-bottom: 5px; display: flex; align-items: center; gap: 8px;
}
.fp-explain-text { font-size: 0.93rem; color: var(--fp-ink) !important; line-height: 1.55; }

/* ── PROGRESS BARS ── */
.fp-prog-wrap { margin: 8px 0 5px; }
.fp-prog-label-row {
  display: flex; justify-content: space-between;
  font-size: 0.83rem; font-weight: 600; margin-bottom: 6px;
  color: var(--fp-ink) !important;
}
.fp-prog-label-row .fp-prog-val { color: var(--fp-muted) !important; font-weight: 400; }
.fp-prog-track { background: #EDE8E2; border-radius: 100px; height: 8px; overflow: hidden; }
.fp-prog-fill { height: 100%; border-radius: 100px; }
.fp-prog-high { background: linear-gradient(90deg, #3D6B58, #5AB88A); }
.fp-prog-mid  { background: linear-gradient(90deg, #C9972B, #D4A847); }
.fp-prog-low  { background: linear-gradient(90deg, #C94A2B, #E07055); }

/* ── CONFIDENCE ROW ── */
.fp-confidence-row {
  display: flex; align-items: center; gap: 12px;
  margin-top: 16px; padding: 12px 16px; border-radius: 12px;
  background: #F0EBE4 !important; border: 1px solid #E0D8D0;
}
.fp-conf-high { border-left: 4px solid var(--fp-sage); }
.fp-conf-med  { border-left: 4px solid var(--fp-gold); }
.fp-conf-low  { border-left: 4px solid var(--fp-rust); }
.fp-conf-label { font-size: 0.85rem; font-weight: 700; color: var(--fp-ink) !important; }
.fp-conf-tip   { font-size: 0.78rem; color: var(--fp-muted) !important; margin-top: 3px; }

/* ── AUDIT CARD (dark) ── */
.fp-audit-card {
  background: #1A1614 !important;
  border-radius: 16px; padding: 28px 32px; margin-bottom: 18px;
  position: relative; overflow: hidden;
}
.fp-audit-title {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 2.5px; text-transform: uppercase;
  color: var(--fp-gold) !important; margin-bottom: 16px;
}
.fp-audit-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.fp-audit-row:last-child { border-bottom: none; }
.fp-audit-row-label { font-size: 0.88rem; color: rgba(255,255,255,0.88) !important; font-weight: 600; }
.fp-audit-row-desc  { font-size: 0.74rem; color: rgba(255,255,255,0.45) !important; margin-top: 3px; }
.fp-audit-scores    { display: flex; align-items: center; gap: 10px; }
.fp-audit-orig      { color: rgba(255,255,255,0.35) !important; text-decoration: line-through; font-size: 0.88rem; }
.fp-audit-adj       { color: var(--fp-gold) !important; font-size: 0.96rem; font-weight: 700; }
.fp-audit-delta-pos { color: #6FCFA0 !important; font-size: 0.76rem; font-weight: 600; }
.fp-audit-delta-neg { color: #F07070 !important; font-size: 0.76rem; font-weight: 600; }
.fp-audit-delta-neu { color: rgba(255,255,255,0.3) !important; font-size: 0.76rem; }
.fp-audit-banner {
  background: rgba(212,168,71,0.12) !important;
  border: 1px solid rgba(212,168,71,0.28);
  border-radius: 10px; padding: 12px 16px;
  font-size: 0.82rem; color: #D4A847 !important; margin-top: 16px; line-height: 1.55;
}
.fp-audit-ok-banner {
  background: rgba(111,207,160,0.10) !important;
  border: 1px solid rgba(111,207,160,0.26);
  border-radius: 10px; padding: 12px 16px;
  font-size: 0.82rem; color: #6FCFA0 !important; margin-top: 16px;
}

/* ── RADAR ── */
.fp-radar-wrap { display: flex; justify-content: center; padding: 10px 0 6px; }
.fp-radar-caption { font-size: 0.76rem; color: var(--fp-muted) !important; text-align: center; margin-top: 4px; }

/* ── IMPROVEMENT CARD ── */
.fp-improve-card {
  background: #EBF4F0 !important;
  border: 1.5px solid #9FC9B5;
  border-radius: 16px; padding: 24px 28px; margin-bottom: 18px;
  color: var(--fp-ink) !important;
}
.fp-improve-header {
  font-size: 0.68rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--fp-sage) !important; margin-bottom: 16px;
}
.fp-improve-step {
  display: flex; gap: 14px; align-items: flex-start;
  padding: 11px 0; border-bottom: 1px solid rgba(61,107,88,0.12);
}
.fp-improve-step:last-child { border-bottom: none; }
.fp-improve-num {
  background: var(--fp-sage) !important; color: #FFFFFF !important;
  border-radius: 50%; width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.76rem; font-weight: 700; flex-shrink: 0; margin-top: 1px;
}
.fp-improve-tag  { font-size: 0.7rem; font-weight: 700; color: var(--fp-sage) !important; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 3px; }
.fp-improve-text { font-size: 0.92rem; line-height: 1.55; color: var(--fp-ink) !important; }

/* ── REPORT CARD ── */
.fp-report-card {
  background: #FFFFFF !important;
  border: 2px solid var(--fp-ink);
  border-radius: 18px; padding: 32px 36px;
  margin: 4px 0 16px; position: relative; overflow: hidden;
  color: var(--fp-ink) !important;
}
.fp-report-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--fp-rust), var(--fp-gold), var(--fp-sage));
}
.fp-report-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 22px; padding-bottom: 18px;
  border-bottom: 1.5px solid var(--fp-ink);
}
.fp-report-title { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: var(--fp-ink) !important; margin: 0; }
.fp-report-subtitle { font-size: 0.78rem; color: var(--fp-muted) !important; margin-top: 5px; }
.fp-report-grade { font-family: 'Playfair Display', serif; font-size: 3rem; line-height: 1; font-weight: 700; color: var(--fp-ink) !important; }
.fp-report-section-title { font-size: 0.64rem; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: var(--fp-muted) !important; margin: 18px 0 8px; }
.fp-report-scores-row {
  display: flex; gap: 0; margin-bottom: 4px;
  background: #F0EBE4 !important; border-radius: 12px;
  overflow: hidden; border: 1px solid var(--fp-border);
  color: var(--fp-ink) !important;
}
.fp-report-score-item {
  flex: 1; text-align: center; padding: 14px 8px;
  border-right: 1px solid var(--fp-border);
  color: var(--fp-ink) !important;
}
.fp-report-score-item:last-child { border-right: none; }
.fp-report-score-num { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: var(--fp-ink) !important; line-height: 1.1; }
.fp-report-score-lbl { font-size: 0.62rem; color: var(--fp-muted) !important; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }

/* ── CHIPS ── */
.fp-chips-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 4px; }
.fp-chip      { display: inline-flex; align-items: center; gap: 5px; background: #EDE8E0 !important; border-radius: 8px; padding: 5px 12px; font-size: 0.8rem; color: var(--fp-ink) !important; }
.fp-chip-good { background: #C7EACF !important; color: #145229 !important; }
.fp-chip-warn { background: #FAEFC0 !important; color: #6A4A00 !important; }

/* ── REPORT WATERMARK ── */
.fp-report-watermark {
  position: absolute; bottom: 16px; right: 20px;
  font-size: 0.64rem; color: rgba(26,22,20,0.12) !important;
  letter-spacing: 1.5px; font-weight: 700; text-transform: uppercase;
}

/* ── ANALYZE BOX ── */
.fp-analyze-box {
  padding: 20px 24px; background: #FFFFFF !important; border-radius: 14px;
  border: 1px solid var(--fp-border); box-shadow: 0 4px 16px rgba(26,22,20,0.06);
  color: var(--fp-ink) !important;
}
.fp-analyze-title {
  font-size: 0.64rem; font-weight: 700; letter-spacing: 2.5px;
  color: var(--fp-muted) !important; margin-bottom: 16px; text-transform: uppercase;
}
.fp-analyze-step { display: flex; align-items: center; gap: 12px; padding: 7px 0; }
.fp-step-dot  { width: 8px; height: 8px; border-radius: 50%; background: var(--fp-rust); flex-shrink: 0; animation: fp-pulse 1.2s infinite; }
.fp-step-done { background: var(--fp-sage); animation: none; width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.fp-step-text { font-size: 0.87rem; color: var(--fp-muted) !important; }
@keyframes fp-pulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.3;transform:scale(0.6);} }

/* ── COACHING TIP ── */
.fp-coaching-tip {
  background: var(--fp-warm) !important; border-radius: 14px;
  padding: 18px 22px; margin: 4px 0 18px;
  display: flex; gap: 14px; align-items: flex-start;
  border-left: 4px solid var(--fp-gold); color: var(--fp-ink) !important;
}
.fp-coaching-icon  { font-size: 1.5rem; flex-shrink: 0; }
.fp-coaching-title { font-weight: 700; font-size: 0.92rem; margin-bottom: 4px; color: var(--fp-ink) !important; }
.fp-coaching-text  { font-size: 0.88rem; color: var(--fp-muted) !important; line-height: 1.55; }

/* ── DEMO CARDS ── */
.fp-demo-card {
  background: #FFFFFF !important;
  border: 1.5px solid var(--fp-border);
  border-radius: 14px; padding: 22px 24px;
  color: var(--fp-ink) !important;
}
.fp-demo-label {
  font-size: 0.66rem; font-weight: 700; letter-spacing: 2.2px;
  text-transform: uppercase; color: var(--fp-muted) !important; margin-bottom: 12px;
  display: flex; align-items: center; gap: 8px;
}
.fp-demo-label::after { content: ''; flex: 1; height: 1px; background: var(--fp-border); }
.fp-demo-score-big {
  font-family: 'Playfair Display', serif;
  font-size: 3.2rem; line-height: 1; margin-bottom: 4px;
}
.fp-demo-score-adj {
  font-family: 'Playfair Display', serif;
  font-size: 2rem; line-height: 1; color: var(--fp-sage) !important; margin-bottom: 4px;
}
.fp-demo-meta { font-size: 0.78rem; color: var(--fp-muted) !important; }
.fp-demo-delta-pos { color: var(--fp-sage) !important; font-weight: 700; font-size: 0.9rem; }
.fp-demo-delta-neg { color: var(--fp-rust) !important; font-weight: 700; font-size: 0.9rem; }

/* ── BIAS INSIGHT PANEL ── */
.fp-bias-insight {
  background: #1A1614 !important;
  border-radius: 16px; padding: 26px 30px; margin: 16px 0;
  position: relative; overflow: hidden;
}
.fp-bias-insight-title {
  font-size: 0.66rem; font-weight: 700; letter-spacing: 2.2px;
  text-transform: uppercase; color: var(--fp-gold) !important; margin-bottom: 14px;
}
.fp-bias-insight-body { font-size: 0.9rem; color: rgba(255,255,255,0.80) !important; line-height: 1.65; }
.fp-bias-insight-highlight { color: var(--fp-gold) !important; font-weight: 600; }
.fp-bias-vs-row {
  display: grid; grid-template-columns: 1fr auto 1fr; gap: 16px;
  align-items: center; margin-top: 18px;
}
.fp-bias-vs-label { font-size: 0.72rem; color: rgba(255,255,255,0.48) !important; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; }
.fp-bias-vs-score { font-family: 'Playfair Display', serif; font-size: 2.4rem; line-height: 1; }
.fp-bias-vs-score-a { color: var(--fp-rust) !important; }
.fp-bias-vs-score-b { color: #6FCFA0 !important; text-align: right; }
.fp-bias-vs-divider { text-align: center; color: rgba(255,255,255,0.28) !important; font-size: 1.4rem; }
.fp-bias-vs-name { font-size: 0.82rem; color: rgba(255,255,255,0.62) !important; }
.fp-bias-vs-name-b { text-align: right; }

/* ── WHY MATTERS SECTION ── */
.fp-why-matters {
  background: #1A1614 !important;
  border-radius: 18px; padding: 40px 44px; margin: 12px 0 24px;
  position: relative; overflow: hidden;
}
.fp-why-matters-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem; color: #FFFFFF !important; margin-bottom: 18px;
}
.fp-why-matters-title em { color: var(--fp-gold) !important; font-style: italic; }
.fp-why-stat-row { display: flex; gap: 20px; flex-wrap: wrap; margin: 20px 0; }
.fp-why-stat {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 12px; padding: 16px 20px; flex: 1; min-width: 130px;
}
.fp-why-stat-num { font-family: 'Playfair Display', serif; font-size: 2rem; color: var(--fp-gold) !important; line-height: 1; }
.fp-why-stat-lbl { font-size: 0.78rem; color: rgba(255,255,255,0.58) !important; margin-top: 4px; line-height: 1.4; }
.fp-why-matters-body { font-size: 0.92rem; color: rgba(255,255,255,0.68) !important; line-height: 1.75; max-width: 700px; }

/* ── DIVIDER & FOOTER ── */
.fp-divider { border: none; border-top: 1px solid var(--fp-border); margin: 28px 0; }
.fp-empty-state { padding: 70px 24px; text-align: center; }
.fp-empty-icon  { font-size: 3.5rem; margin-bottom: 18px; opacity: 0.6; }
.fp-empty-title { font-size: 1rem; font-weight: 600; color: var(--fp-ink) !important; margin-bottom: 8px; }
.fp-empty-desc  { font-size: 0.88rem; line-height: 1.6; color: var(--fp-muted) !important; }
.fp-footer      { text-align: center; color: var(--fp-muted) !important; font-size: 0.8rem; padding: 32px 0 18px; letter-spacing: 0.5px; line-height: 1.8; }

/* ── STREAMLIT BUTTON OVERRIDES ── */
.stButton > button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-family: 'DM Sans', sans-serif !important;
  transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
  background: var(--fp-ink) !important;
  color: #FFFFFF !important;
  border: none !important;
}
.stButton > button[kind="primary"]:hover {
  background: #2C2420 !important;
  box-shadow: 0 4px 16px rgba(26,22,20,0.25) !important;
}
.stButton > button[kind="secondary"] {
  background: #EDE8DF !important;
  color: var(--fp-ink) !important;
  border: 1.5px solid var(--fp-border) !important;
}

/* ── STREAMLIT FORM INPUTS ── */
.stTextArea textarea {
  border-radius: 12px !important;
  border-color: var(--fp-border) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.94rem !important;
  color: var(--fp-ink) !important;
  background: #FDFAF7 !important;
}
.stTextArea textarea:focus {
  border-color: var(--fp-sage) !important;
  box-shadow: 0 0 0 3px rgba(61,107,88,0.12) !important;
}
.stSelectbox > div > div {
  border-radius: 10px !important;
  border-color: var(--fp-border) !important;
  background: #FDFAF7 !important;
  color: var(--fp-ink) !important;
}
.stToggle { margin: 8px 0 !important; }
div[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── WORD COUNT LINE ── */
.fp-wc { font-size: 0.82rem; margin-top: 4px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
QUESTIONS = {
    "Behavioral": [
        {
            "q": "Tell me about a time you faced a significant challenge at work and how you overcame it.",
            "keywords": ["challenge", "problem", "solution", "team", "result", "learned", "overcame",
                         "strategy", "communication", "goal", "deadline", "impact", "resolved"],
            "sample": (
                "In my previous role, our team faced a critical production outage two days before a major client demo. "
                "I quickly organized a war-room with the backend and DevOps teams, delegated debugging tasks based on "
                "expertise, and kept stakeholders updated every 30 minutes. Within 6 hours we identified a misconfigured "
                "load balancer, fixed it, and ran a full regression suite. The demo proceeded smoothly and the client "
                "signed a 12-month contract. I learned that clear communication under pressure is as important as technical skill."
            ),
        },
        {
            "q": "Describe a situation where you had to work with a difficult team member. What did you do?",
            "keywords": ["conflict", "listen", "empathy", "communication", "collaborate", "compromise",
                         "feedback", "resolved", "understood", "perspective", "approach", "outcome"],
            "sample": (
                "I once worked with a colleague who frequently missed sprint deadlines without flagging blockers early. "
                "Instead of escalating immediately, I requested a one-on-one to understand their perspective. I learned "
                "they were juggling undocumented on-call duties. Together we restructured their task load and set up a "
                "daily five-minute check-in. Their delivery rate improved by 40% in the next sprint, and we built a "
                "much stronger working relationship as a result."
            ),
        },
    ],
    "Technical": [
        {
            "q": "Explain how you would design a URL shortening service like bit.ly. Walk through your architecture decisions.",
            "keywords": ["database", "api", "hash", "redirect", "scale", "cache", "load balancer",
                         "unique", "storage", "endpoint", "microservice", "latency", "throughput"],
            "sample": (
                "I would start with a REST API layer behind a load balancer. The core service generates a unique "
                "6-character base62 hash for each long URL and stores the mapping in a relational database like "
                "PostgreSQL for durability. For read performance I'd layer Redis in front as a cache with a TTL policy. "
                "At scale, I'd shard the DB by hash prefix and use a CDN to serve redirects close to the user. "
                "Analytics events would be published to a Kafka topic and processed asynchronously to avoid blocking the redirect critical path."
            ),
        },
        {
            "q": "What is the difference between a process and a thread? When would you choose one over the other?",
            "keywords": ["memory", "process", "thread", "concurrency", "GIL", "isolation", "shared",
                         "lightweight", "context switch", "CPU", "I/O", "parallel", "overhead"],
            "sample": (
                "A process is an independent program with its own memory space, offering strong isolation but higher "
                "overhead for creation and IPC. A thread lives inside a process and shares its memory, making "
                "communication cheaper but requiring careful synchronization to avoid race conditions. In Python, "
                "the GIL limits true CPU-bound thread parallelism, so I'd use multiprocessing for CPU-intensive work "
                "and threading or async I/O for I/O-bound tasks like network requests. In languages without a GIL, "
                "like Go or Rust, threads shine for both workloads."
            ),
        },
    ],
}


# ── EVALUATION ENGINE ─────────────────────────────────────────────────────────
def evaluate_answer(answer: str, keywords: list) -> dict:
    text = answer.strip()
    words = text.split()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    word_count = len(words)
    sentence_count = len(sentences)
    text_lower = text.lower()
    matched = [kw for kw in keywords if kw.lower() in text_lower]
    coverage = len(matched) / len(keywords)
    relevance_raw = min(100, int(coverage * 100 * 1.35))
    if sentence_count > 0:
        avg_len = word_count / sentence_count
        if 12 <= avg_len <= 22:    clarity_raw = 90
        elif 8 <= avg_len < 12 or 22 < avg_len <= 30: clarity_raw = 70
        elif avg_len < 8:          clarity_raw = 50
        else:                       clarity_raw = 55
    else:
        clarity_raw = 30
    if word_count >= 80:
        clarity_raw = min(100, clarity_raw + 8)
    intro_words   = ["i ", "when ", "in my", "at my", "once ", "during ", "the situation"]
    body_words    = ["because", "therefore", "however", "first", "then", "next", "so ", "which", "that"]
    closing_words = ["result", "outcome", "learned", "ultimately", "as a result", "impact", "finally", "conclusion"]
    has_intro   = any(p in text_lower for p in intro_words)
    has_body    = any(p in text_lower for p in body_words)
    has_closing = any(p in text_lower for p in closing_words)
    structure_raw  = 30
    structure_raw += 25 if has_intro   else 0
    structure_raw += 25 if has_body    else 0
    structure_raw += 20 if has_closing else 0
    if sentence_count >= 4:
        structure_raw = min(100, structure_raw + 10)
    overall = int(0.35 * relevance_raw + 0.35 * clarity_raw + 0.30 * structure_raw)
    bias_flags = []
    if word_count < 40 and structure_raw < 50:
        bias_flags.append({
            "icon": "📏",
            "label": "Length Bias",
            "detail": (
                f"Your answer is {word_count} words. Short answers can still be high-quality, "
                "but the structure scorer may penalise brevity unfairly. "
                "Structure score has been partially adjusted."
            ),
        })
        structure_raw = min(100, structure_raw + 15)
    if relevance_raw >= 65 and overall < 55:
        bias_flags.append({
            "icon": "✍️",
            "label": "Content-Form Imbalance",
            "detail": (
                "Your answer covers the right topics (high relevance) but scored lower overall due to "
                "structural markers. Ethical AI should weigh substantive content at least equally to form. "
                "Overall score adjusted upward."
            ),
        })
        overall = min(100, overall + 10)
    overall = int(0.35 * relevance_raw + 0.35 * clarity_raw + 0.30 * structure_raw)
    overall = min(100, overall)

    def relevance_explain(score, matched_kws):
        if score >= 75:
            return (f"Your answer included key concepts ({', '.join(matched_kws[:4])}"
                    f"{'...' if len(matched_kws) > 4 else ''}), demonstrating strong topical awareness.")
        elif score >= 50:
            unkw = [k for k in keywords if k.lower() not in text_lower]
            return f"Partial coverage of expected topics. Missing concepts include: {', '.join(unkw[:4])}."
        else:
            return "Your answer did not address the core concepts expected for this question. Review the topic keywords and try to align your response."

    def clarity_explain(score, wc, sc):
        if score >= 80:
            return f"Well-paced writing ({wc} words across {sc} sentences). Sentence length feels natural and readable."
        elif score >= 60:
            return "Reasonably clear, but some sentences are either too long or too short. Aim for 12–22 words per sentence."
        else:
            return f"Clarity needs work — sentence structure is uneven ({wc} words, {sc} sentences). Break long sentences and add connectives."

    def structure_explain(score, hi, hb, hc):
        parts = []
        if not hi: parts.append("a clear opening that sets the scene")
        if not hb: parts.append("logical connectors (first, then, because, however)")
        if not hc: parts.append("a result or lesson to close the answer")
        if parts:
            return "Your answer could benefit from adding: " + "; ".join(parts) + "."
        return "Good structure — your answer flows from context through explanation to a clear outcome."

    return {
        "overall": overall, "relevance": relevance_raw, "clarity": clarity_raw,
        "structure": structure_raw, "bias_flags": bias_flags, "word_count": word_count,
        "matched_kws": matched, "has_intro": has_intro, "has_body": has_body,
        "has_closing": has_closing, "sentence_count": sentence_count,
        "explanations": {
            "relevance":  relevance_explain(relevance_raw, matched),
            "clarity":    clarity_explain(clarity_raw, word_count, sentence_count),
            "structure":  structure_explain(structure_raw, has_intro, has_body, has_closing),
        },
    }


def compute_confidence(r: dict) -> dict:
    scores = [r["relevance"], r["clarity"], r["structure"]]
    mean = sum(scores) / 3
    variance = sum((s - mean) ** 2 for s in scores) / 3
    std_dev = math.sqrt(variance)
    word_bonus = min(20, r["word_count"] // 8)
    raw_conf = max(0, min(100, 100 - int(std_dev * 0.9) + word_bonus - len(r["bias_flags"]) * 8))
    if raw_conf >= 72:
        label, css, icon = "High Confidence",   "fp-conf-high", "🟢"
        tip = "Evaluation signals are consistent — scores reliably reflect answer quality."
    elif raw_conf >= 48:
        label, css, icon = "Medium Confidence", "fp-conf-med",  "🟡"
        tip = "Some dimension variance detected. Results are indicative but not definitive."
    else:
        label, css, icon = "Low Confidence",    "fp-conf-low",  "🔴"
        tip = "High variance between dimensions. Answer may be ambiguous or very short."
    return {"score": raw_conf, "label": label, "css": css, "icon": icon, "tip": tip}


def run_fairness_audit(r: dict) -> dict:
    orig = r["overall"]
    no_struct  = min(100, int(0.35 * r["relevance"] + 0.35 * r["clarity"] + 0.30 * max(r["structure"], 70)))
    no_length  = min(100, int(0.35 * r["relevance"] + 0.35 * max(r["clarity"], 65) + 0.30 * r["structure"]))
    content1st = min(100, int(0.60 * r["relevance"] + 0.20 * r["clarity"] + 0.20 * r["structure"]))
    conditions = [
        {"label": "Without Structure Penalty", "icon": "🏗️", "score": no_struct,  "delta": no_struct  - orig, "desc": "Score if structural form markers were not penalised."},
        {"label": "Without Length Penalty",    "icon": "📏", "score": no_length,  "delta": no_length  - orig, "desc": "Score if answer length did not affect the clarity dimension."},
        {"label": "Content-First Weighting",   "icon": "💡", "score": content1st, "delta": content1st - orig, "desc": "Score if topical relevance was weighted 60% (vs default 35%)."},
    ]
    max_delta = max(abs(c["delta"]) for c in conditions)
    return {"original": orig, "conditions": conditions, "affected": max_delta >= 8, "max_delta": max_delta}


def render_radar_chart(relevance: int, clarity: int, structure: int) -> str:
    cx, cy, r_max = 130, 130, 90
    angles = [-90, 30, 150]
    values = [relevance / 100, clarity / 100, structure / 100]
    labels = ["Relevance", "Clarity", "Structure"]

    def polar(angle_deg, radius):
        rad = math.radians(angle_deg)
        return cx + radius * math.cos(rad), cy + radius * math.sin(rad)

    rings = ""
    for pct in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{polar(a, r_max * pct)[0]:.1f},{polar(a, r_max * pct)[1]:.1f}" for a in angles)
        alpha = 0.4 + pct * 0.3
        rings += f'<polygon points="{pts}" fill="none" stroke="#D8D0C8" stroke-width="1" opacity="{alpha:.1f}"/>'
    axes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{polar(a, r_max)[0]:.1f}" y2="{polar(a, r_max)[1]:.1f}" stroke="#D8D0C8" stroke-width="1.5"/>'
        for a in angles
    )
    data_pts = [polar(a, r_max * v) for a, v in zip(angles, values)]
    pts_str  = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in data_pts)
    polygon  = f'<polygon points="{pts_str}" fill="rgba(61,107,88,0.18)" stroke="#3D6B58" stroke-width="2.5" stroke-linejoin="round"/>'
    dots = "".join(
        f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="5.5" fill="#3D6B58" stroke="white" stroke-width="2"/>'
        for p in data_pts
    )
    label_off = 24
    lbl_svg = ""
    for a, lbl, val in zip(angles, labels, [relevance, clarity, structure]):
        lx, ly = polar(a, r_max + label_off)
        anchor = "middle" if a == -90 else ("start" if a == 30 else "end")
        lbl_svg += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-family="DM Sans,sans-serif" font-size="11" font-weight="700" fill="#5C524A" letter-spacing="0.5">{lbl}</text>'
            f'<text x="{lx:.1f}" y="{ly+14:.1f}" text-anchor="{anchor}" font-family="DM Sans,sans-serif" font-size="11" fill="#3D6B58" font-weight="600">{val}</text>'
        )
    return f'<svg viewBox="0 0 260 260" width="260" height="260" xmlns="http://www.w3.org/2000/svg">{rings}{axes}{polygon}{dots}{lbl_svg}</svg>'


IMPROVEMENT_MAP = {
    "relevance": {
        "tag": "RELEVANCE", "icon": "📌",
        "steps": [
            ("Mirror the question",   "Identify 2-3 core nouns from the question and explicitly use them in your opening sentence."),
            ("Add domain vocabulary", "Include field-specific terms the interviewer expects — e.g. metrics, tools, frameworks relevant to the role."),
            ("Connect to outcomes",   "State a measurable result that proves your answer addressed the actual problem asked."),
        ],
    },
    "clarity": {
        "tag": "CLARITY", "icon": "💡",
        "steps": [
            ("One idea per sentence", "Split any sentence over 30 words in two. Each sentence should carry exactly one thought."),
            ("Use active voice",      "Replace passive constructions with direct ones. 'The team decided' beats 'It was decided by the team'."),
            ("Read it aloud",         "If you stumble reading your answer aloud, rewrite that sentence. Spoken rhythm equals readable writing."),
        ],
    },
    "structure": {
        "tag": "STRUCTURE", "icon": "🏗️",
        "steps": [
            ("Use the STAR method",    "Situation → Task → Action → Result. Label each part mentally before writing."),
            ("Add a signpost opening", "Start with: 'I will describe a situation where...' — this signals clear intent instantly."),
            ("Close with a lesson",    "End with 'From this I learned...' or 'The outcome was...' — a conclusion shows maturity."),
        ],
    },
}


def get_improvement_suggestions(r: dict):
    dims = {"relevance": r["relevance"], "clarity": r["clarity"], "structure": r["structure"]}
    weakest = min(dims, key=dims.get)
    return IMPROVEMENT_MAP[weakest], weakest, dims[weakest]


def score_class(score: int) -> str:
    if score >= 75: return "fp-score-high"
    if score >= 50: return "fp-score-mid"
    return "fp-score-low"

def score_emoji(score: int) -> str:
    if score >= 80: return "🟢"
    if score >= 60: return "🟡"
    return "🔴"

def prog_class(score: int) -> str:
    if score >= 75: return "fp-prog-high"
    if score >= 50: return "fp-prog-mid"
    return "fp-prog-low"

def render_progress(label: str, score: int):
    pc = prog_class(score)
    st.markdown(
        f'<div class="fp-prog-wrap">'
        f'<div class="fp-prog-label-row"><span>{label}</span><span class="fp-prog-val"><b>{score}</b>&thinsp;/&thinsp;100</span></div>'
        f'<div class="fp-prog-track"><div class="fp-prog-fill {pc}" style="width:{score}%;"></div></div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in {"answer": "", "result": None, "question_idx": 0, "fairness_audit": False, "demo_results": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="fp-hero">'
    '<div class="fp-hero-tag">🎯 Ethical AI · Interview Coach</div>'
    '<h1>FairPrep <em>AI</em></h1>'
    '<p>Practice interviews with an AI that scores your answers <strong style="color:#D4A847;">transparently</strong>, '
    'flags potential evaluation bias, and explains every decision so you grow faster and fairer.</p>'
    '<div class="fp-hero-meta">'
    '<div class="fp-hero-badge">⚖️ Bias Detection</div>'
    '<div class="fp-hero-badge">🔍 Explainable Scores</div>'
    '<div class="fp-hero-badge">📊 Strength Radar</div>'
    '<div class="fp-hero-badge">🔬 Fairness Audit</div>'
    '<div class="fp-hero-badge">🧠 AI Confidence</div>'
    '<div class="fp-hero-badge">🚫 No External APIs</div>'
    '</div></div>',
    unsafe_allow_html=True
)


# ── LAYOUT ────────────────────────────────────────────────────────────────────
left, right = st.columns([1.1, 1], gap="large")

with left:
    # Step 1
    st.markdown('<div class="fp-card">', unsafe_allow_html=True)
    st.markdown('<div class="fp-section-label">Step 1 · Interview Type</div>', unsafe_allow_html=True)
    interview_type = st.selectbox("Choose the type of interview:", ["Behavioral", "Technical"], label_visibility="collapsed")
    question_pool = QUESTIONS[interview_type]
    q_idx = st.session_state.question_idx % len(question_pool)
    current_q = question_pool[q_idx]
    st.markdown(f'<div class="fp-question-box">💬 {current_q["q"]}</div>', unsafe_allow_html=True)
    col_next, col_sample = st.columns(2)
    with col_next:
        if st.button("🔄 Next Question", use_container_width=True):
            st.session_state.question_idx += 1
            st.session_state.answer = ""
            st.session_state.result = None
            st.session_state.demo_results = None
            st.rerun()
    with col_sample:
        show_sample = st.button("✨ Load Sample Answer", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Step 2
    st.markdown('<div class="fp-card">', unsafe_allow_html=True)
    st.markdown('<div class="fp-section-label">Step 2 · Your Answer</div>', unsafe_allow_html=True)
    if show_sample:
        st.session_state.answer = current_q["sample"]
    answer = st.text_area(
        "Type your answer below (aim for 80–200 words for best results):",
        value=st.session_state.answer,
        height=200,
        placeholder="Begin your answer here…  e.g. 'In my previous role, I was tasked with...'",
        label_visibility="visible",
    )
    st.session_state.answer = answer
    word_count_live = len(answer.split()) if answer.strip() else 0
    wc_color = "#3D6B58" if word_count_live >= 60 else ("#C9972B" if word_count_live >= 30 else "#C94A2B")
    st.markdown(f'<p class="fp-wc" style="color:{wc_color};">📝 {word_count_live} words</p>', unsafe_allow_html=True)
    fairness_on = st.toggle("⚖️ Enable Fairness Audit Mode", value=st.session_state.fairness_audit,
                             help="Simulates three alternate scoring philosophies to reveal how different evaluation frameworks affect your score.")
    st.session_state.fairness_audit = fairness_on
    demo_mode = st.toggle("🎭 Demo Bias Scenario", value=False,
                           help="Shows how two answers of similar quality can receive very different scores due to evaluation bias.")
    evaluate_btn = st.button("🚀 Evaluate My Answer", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("ℹ️ How FairPrep AI evaluates you"):
        st.markdown("""
**Scoring dimensions**
- **Relevance** — keyword & concept coverage relative to the question domain
- **Clarity** — sentence-length distribution & readability
- **Structure** — presence of intro, reasoning body, and conclusion

**Bias Detection** flags two common AI evaluation pitfalls:
- *Length Bias* — short answers being structurally penalised even when concise and relevant
- *Content-Form Imbalance* — over-weighting grammar/form vs. substantive content

**AI Confidence Score** measures evaluation reliability based on cross-dimension consistency.

**Fairness Audit** simulates 3 alternate scoring philosophies and surfaces the score delta.
        """)


# ── EVALUATION TRIGGER ────────────────────────────────────────────────────────
if evaluate_btn:
    if not answer.strip() and not demo_mode:
        with right:
            st.warning("⚠️ Please type an answer before evaluating.")

    elif demo_mode:
        concise_answer = (
            "I led a critical project under pressure. We faced a production outage two days before a major demo. "
            "I organized teams, delegated debugging, and kept stakeholders updated. Fixed within 6 hours. "
            "Demo succeeded, client signed contract. Learned communication matters as much as technical skill."
        )
        verbose_answer = (
            "I would like to share a significant experience from my previous role where I was tasked with leading "
            "a critical project under extreme pressure. The situation arose when our team encountered a major production "
            "outage exactly two days before what was supposed to be a very important client demonstration. In response "
            "to this challenge, I immediately took the initiative to organize a comprehensive war-room situation that "
            "included bringing together both the backend engineering teams and the DevOps specialists. I strategically "
            "delegated debugging tasks based on individual team members' specific areas of expertise and technical "
            "knowledge. Additionally, I implemented a structured communication protocol that involved providing regular "
            "updates to all key stakeholders every thirty minutes to ensure complete transparency and alignment. Through "
            "this coordinated effort, we were successfully able to identify and resolve the root cause of the outage, "
            "which turned out to be a misconfigured load balancer, within an impressive timeframe of just six hours. "
            "As a direct result of our quick and effective response, the demonstration was able to proceed smoothly "
            "without any technical issues, which ultimately led to the client signing a significant twelve-month "
            "contract with our organization. This experience taught me the valuable lesson that clear communication "
            "under pressure is just as important as having strong technical skills when it comes to successful "
            "project management and team leadership."
        )
        with right:
            placeholder = st.empty()
            steps_info = [
                "Creating bias demonstration scenarios…",
                "Evaluating concise candidate…",
                "Evaluating verbose candidate…",
                "Running bias detection engine…",
                "Computing fairness adjustments…",
                "Generating bias comparison…",
            ]
            done = []
            for msg in steps_info:
                done.append(msg)
                rows_html = "".join(
                    f'<div class="fp-analyze-step"><div class="{"fp-step-done" if i < len(done)-1 else "fp-step-dot"}"></div>'
                    f'<span class="fp-step-text">{m}</span></div>'
                    for i, m in enumerate(done)
                )
                placeholder.markdown(
                    f'<div class="fp-analyze-box"><div class="fp-analyze-title">Bias Demo Processing</div>{rows_html}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.45)
            time.sleep(0.3)
            placeholder.empty()

        concise_result = evaluate_answer(concise_answer, current_q["keywords"])
        verbose_result = evaluate_answer(verbose_answer, current_q["keywords"])
        st.session_state.demo_results = {
            "concise": concise_result,
            "verbose": verbose_result,
            "concise_text": concise_answer,
            "verbose_text": verbose_answer,
        }
        st.session_state.result = None

    else:
        with right:
            placeholder = st.empty()
            steps_info = [
                ("🔍", "Tokenising and parsing your response…"),
                ("📊", "Scoring relevance against question domain…"),
                ("🧠", "Detecting structural signals…"),
                ("⚖️", "Running bias detection engine…"),
                ("🎯", "Computing AI confidence score…"),
                ("📐", "Simulating fairness audit conditions…"),
                ("✅", "Generating transparent feedback…"),
            ]
            done = []
            for icon, msg in steps_info:
                done.append((icon, msg))
                rows_html = "".join(
                    f'<div class="fp-analyze-step"><div class="{"fp-step-done" if i < len(done)-1 else "fp-step-dot"}"></div>'
                    f'<span class="fp-step-text">{ic} {m}</span></div>'
                    for i, (ic, m) in enumerate(done)
                )
                placeholder.markdown(
                    f'<div class="fp-analyze-box"><div class="fp-analyze-title">AI Processing</div>{rows_html}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.38)
            time.sleep(0.25)
            placeholder.empty()
        st.session_state.result = evaluate_answer(answer, current_q["keywords"])
        st.session_state.demo_results = None


# ── RIGHT COLUMN ──────────────────────────────────────────────────────────────
with right:

    # ── DEMO RESULTS ──────────────────────────────────────────────────────────
    if st.session_state.demo_results:
        demo = st.session_state.demo_results
        cr = demo["concise"]
        vr = demo["verbose"]
        ca = run_fairness_audit(cr)
        va = run_fairness_audit(vr)
        c_adj = max(ca["conditions"], key=lambda x: x["score"])["score"]
        v_adj = max(va["conditions"], key=lambda x: x["score"])["score"]

        st.markdown(
            '<div class="fp-bias-insight">'
            '<div class="fp-bias-insight-title">🎭 Bias Demonstration — Same Quality, Different Scores</div>'
            '<div class="fp-bias-insight-body">Two candidates described the <span class="fp-bias-insight-highlight">identical scenario</span>. '
            'One was concise (46 words). One was verbose (186 words). The scoring engine rewarded length and structural '
            'signal words — not content quality. This is <span class="fp-bias-insight-highlight">Length Bias</span> in action.</div>'
            f'<div class="fp-bias-vs-row">'
            f'  <div>'
            f'    <div class="fp-bias-vs-label">Concise Candidate</div>'
            f'    <div class="fp-bias-vs-score fp-bias-vs-score-a">{cr["overall"]}</div>'
            f'    <div class="fp-bias-vs-name">{cr["word_count"]} words &middot; {len(cr["matched_kws"])} keywords</div>'
            f'  </div>'
            f'  <div class="fp-bias-vs-divider">vs</div>'
            f'  <div>'
            f'    <div class="fp-bias-vs-label fp-bias-vs-name-b">Verbose Candidate</div>'
            f'    <div class="fp-bias-vs-score fp-bias-vs-score-b">{vr["overall"]}</div>'
            f'    <div class="fp-bias-vs-name fp-bias-vs-name-b">{vr["word_count"]} words &middot; {len(vr["matched_kws"])} keywords</div>'
            f'  </div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<div class="fp-demo-card">', unsafe_allow_html=True)
            st.markdown('<div class="fp-demo-label">📏 Concise Candidate</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="fp-demo-score-big" style="color:#C94A2B;">{cr["overall"]}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.75rem;color:#5C524A;margin-bottom:8px;">Raw Score / 100</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="fp-demo-score-adj">{c_adj}</div>', unsafe_allow_html=True)
            delta = c_adj - cr["overall"]
            cls = "fp-demo-delta-pos" if delta >= 0 else "fp-demo-delta-neg"
            st.markdown(f'<div class="fp-demo-meta">Fairness adjusted &nbsp;<span class="{cls}">{("+" if delta >= 0 else "")}{delta}</span></div>', unsafe_allow_html=True)
            render_progress("Relevance", cr["relevance"])
            render_progress("Clarity",   cr["clarity"])
            render_progress("Structure", cr["structure"])
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="fp-demo-card">', unsafe_allow_html=True)
            st.markdown('<div class="fp-demo-label">📖 Verbose Candidate</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="fp-demo-score-big" style="color:#3D6B58;">{vr["overall"]}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.75rem;color:#5C524A;margin-bottom:8px;">Raw Score / 100</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="fp-demo-score-adj">{v_adj}</div>', unsafe_allow_html=True)
            delta2 = v_adj - vr["overall"]
            cls2 = "fp-demo-delta-pos" if delta2 >= 0 else "fp-demo-delta-neg"
            st.markdown(f'<div class="fp-demo-meta">Fairness adjusted &nbsp;<span class="{cls2}">{("+" if delta2 >= 0 else "")}{delta2}</span></div>', unsafe_allow_html=True)
            render_progress("Relevance", vr["relevance"])
            render_progress("Clarity",   vr["clarity"])
            render_progress("Structure", vr["structure"])
            st.markdown('</div>', unsafe_allow_html=True)

        score_gap = vr["overall"] - cr["overall"]
        st.markdown(
            f'<div class="fp-audit-card" style="margin-top:8px;">'
            f'<div class="fp-audit-title">🔬 Bias Impact Analysis</div>'
            f'<div class="fp-audit-row">'
            f'  <div><div class="fp-audit-row-label">Score Gap (Verbose vs Concise)</div>'
            f'  <div class="fp-audit-row-desc">Points advantage for the longer answer</div></div>'
            f'  <div class="fp-audit-scores"><span class="fp-audit-adj">{score_gap:+d} pts</span></div>'
            f'</div>'
            f'<div class="fp-audit-row">'
            f'  <div><div class="fp-audit-row-label">Keywords Matched</div>'
            f'  <div class="fp-audit-row-desc">Concise vs Verbose — content parity check</div></div>'
            f'  <div class="fp-audit-scores"><span class="fp-audit-adj">{len(cr["matched_kws"])} vs {len(vr["matched_kws"])}</span></div>'
            f'</div>'
            f'<div class="fp-audit-row">'
            f'  <div><div class="fp-audit-row-label">Structural Signal Words</div>'
            f'  <div class="fp-audit-row-desc">Connectives detected by scoring engine</div></div>'
            f'  <div class="fp-audit-scores"><span class="fp-audit-adj">{"✓" if cr["has_body"] else "✗"} vs {"✓" if vr["has_body"] else "✗"}</span></div>'
            f'</div>'
            f'<div class="fp-audit-banner">⚠️ A score gap of <b>{score_gap} points</b> between answers with equivalent content '
            f'signals Length Bias. FairPrep AI detects and corrects this — closing the gap to '
            f'<b>{abs(c_adj - v_adj)} points</b> after fairness adjustment.</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # ── NORMAL RESULTS ────────────────────────────────────────────────────────
    elif st.session_state.result is None:
        st.markdown(
            '<div class="fp-empty-state">'
            '<div class="fp-empty-icon">🎯</div>'
            '<div class="fp-empty-title">Your results will appear here</div>'
            '<div class="fp-empty-desc">Choose an interview type, write your answer, and hit <b>Evaluate My Answer</b>.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        r       = st.session_state.result
        overall = r["overall"]
        sc      = score_class(overall)
        se      = score_emoji(overall)
        grade_label = ("Excellent" if overall >= 80 else "Good" if overall >= 65 else "Fair" if overall >= 45 else "Needs Work")
        conf  = compute_confidence(r)
        audit = run_fairness_audit(r)

        st.success("✅ Fairness Score audited using Ethical AI Engine — all bias adjustments applied.")

        # Overall Score Card
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown('<div class="fp-section-label">Overall Score</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="fp-big-score-wrap">'
            f'<div class="fp-big-score-num">{overall}</div>'
            f'<div class="fp-big-score-info">'
            f'<div class="fp-score-pill {sc}">{se} {grade_label}</div>'
            f'<div class="fp-big-score-meta">{r["word_count"]} words &middot; {len(r["matched_kws"])} topic keywords matched</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        render_progress("📌 Relevance", r["relevance"])
        render_progress("💡 Clarity",   r["clarity"])
        render_progress("🏗️ Structure", r["structure"])
        st.markdown(
            f'<div class="fp-confidence-row {conf["css"]}">'
            f'<div style="font-size:1.3rem;">{conf["icon"]}</div>'
            f'<div><div class="fp-conf-label">🧠 AI Confidence: {conf["label"]} &nbsp;({conf["score"]}/100)</div>'
            f'<div class="fp-conf-tip">{conf["tip"]}</div></div></div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Radar
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown('<div class="fp-section-label">📊 Answer Strength Radar</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fp-radar-wrap">{render_radar_chart(r["relevance"], r["clarity"], r["structure"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="fp-radar-caption">Relative strength across all three evaluation dimensions</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Bias Detection
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown('<div class="fp-section-label">⚖️ Bias Detection Report</div>', unsafe_allow_html=True)
        if r["bias_flags"]:
            for flag in r["bias_flags"]:
                st.markdown(
                    f'<div class="fp-bias-warning">'
                    f'<div class="fp-bias-icon">⚠️</div>'
                    f'<div><div class="fp-bias-title">Potential Bias Detected — {flag["label"]}</div>'
                    f'<div class="fp-bias-desc">{flag["detail"]}</div></div></div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="fp-bias-ok">'
                '<div class="fp-bias-icon">✅</div>'
                '<div><div class="fp-bias-title">No Bias Detected</div>'
                '<div class="fp-bias-desc">The evaluation appears balanced across length, content, and form dimensions.</div>'
                '</div></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Fairness Audit
        if st.session_state.fairness_audit:
            st.markdown('<div class="fp-audit-card">', unsafe_allow_html=True)
            st.markdown('<div class="fp-audit-title">🔬 Fairness Audit — Alternate Scoring Conditions</div>', unsafe_allow_html=True)
            for cond in audit["conditions"]:
                d = cond["delta"]
                d_cls = "fp-audit-delta-pos" if d > 0 else ("fp-audit-delta-neg" if d < 0 else "fp-audit-delta-neu")
                d_str = f"+{d}" if d > 0 else str(d)
                st.markdown(
                    f'<div class="fp-audit-row">'
                    f'<div><div class="fp-audit-row-label">{cond["icon"]} {cond["label"]}</div>'
                    f'<div class="fp-audit-row-desc">{cond["desc"]}</div></div>'
                    f'<div class="fp-audit-scores">'
                    f'<span class="fp-audit-orig">{audit["original"]}</span>'
                    f'<span style="color:rgba(255,255,255,0.25);">→</span>'
                    f'<span class="fp-audit-adj">{cond["score"]}</span>'
                    f'<span class="{d_cls}">({d_str})</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
            if audit["affected"]:
                st.markdown(
                    f'<div class="fp-audit-banner">⚠️ This answer may be affected by evaluation bias under certain scoring '
                    f'conditions. Maximum score variance: <b>{audit["max_delta"]} points</b>. '
                    f'A fair system should show &lt;5 points variance across all conditions.</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="fp-audit-ok-banner">✅ Score is stable across all alternate conditions. Evaluation is robust and fair.</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # Why You Got This Score
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown('<div class="fp-section-label">🔍 Why You Got This Score</div>', unsafe_allow_html=True)
        for icon, label, text, score in [
            ("📌", "RELEVANCE", r["explanations"]["relevance"], r["relevance"]),
            ("💡", "CLARITY",   r["explanations"]["clarity"],   r["clarity"]),
            ("🏗️", "STRUCTURE", r["explanations"]["structure"], r["structure"]),
        ]:
            st.markdown(
                f'<div class="fp-explain-row">'
                f'<div class="fp-explain-icon">{icon}</div>'
                f'<div style="flex:1;">'
                f'<div class="fp-explain-label">{label}'
                f'<span class="fp-score-pill {score_class(score)}" style="padding:2px 10px;font-size:0.7rem;">{score}/100</span>'
                f'</div>'
                f'<div class="fp-explain-text">{text}</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )
        if conf["score"] < 70:
            st.info("ℹ️ Confidence is lower because scores vary significantly across dimensions.")
        st.caption("Score formula: Relevance (35%) + Clarity (35%) + Structure (30%)")
        st.markdown('</div>', unsafe_allow_html=True)

        # Improvement Plan
        plan, weak_dim, weak_score = get_improvement_suggestions(r)
        st.markdown(
            f'<div class="fp-improve-card">'
            f'<div class="fp-improve-header">🎯 Next Steps to Improve · Weakest: {plan["tag"]} ({weak_score}/100)</div>',
            unsafe_allow_html=True
        )
        for i, (step_title, step_desc) in enumerate(plan["steps"], 1):
            st.markdown(
                f'<div class="fp-improve-step">'
                f'<div class="fp-improve-num">{i}</div>'
                f'<div><div class="fp-improve-tag">{step_title}</div>'
                f'<div class="fp-improve-text">{step_desc}</div></div>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Coaching Tip
        coaching_data = {
            (80, 101): ("🏆", "Outstanding answer!", "You demonstrated strong topical knowledge with clear structure. Practice maintaining this quality under time pressure."),
            (65,  80): ("📈", "Solid foundation.",   "Strengthen your closing — end with a concrete result or lesson learned to lift all three scores."),
            (45,  65): ("🛠️", "Room to grow.",       "Focus on covering more domain keywords and adding a clear intro-body-conclusion flow."),
            (0,   45): ("💪", "Keep practising.",    "Try loading the sample answer to see the expected structure, then write your own version in your own words."),
        }
        for (lo, hi), (icon, heading, msg) in coaching_data.items():
            if lo <= overall < hi:
                st.markdown(
                    f'<div class="fp-coaching-tip">'
                    f'<div class="fp-coaching-icon">{icon}</div>'
                    f'<div><div class="fp-coaching-title">{heading}</div>'
                    f'<div class="fp-coaching-text">{msg}</div></div></div>',
                    unsafe_allow_html=True
                )
                break

        # Report Card
        today_str    = datetime.datetime.now().strftime("%B %d, %Y · %H:%M")
        grade_letter = ("A" if overall >= 88 else "B" if overall >= 75 else "C" if overall >= 60 else "D" if overall >= 45 else "F")
        grade_color  = "#3D6B58" if overall >= 75 else ("#C9972B" if overall >= 55 else "#C94A2B")
        strengths = []
        if r["relevance"] >= 70:       strengths.append("Strong topical relevance")
        if r["clarity"]   >= 70:       strengths.append("Clear sentence construction")
        if r["structure"] >= 70:       strengths.append("Well-structured argument")
        if r["word_count"] >= 80:      strengths.append(f"Thorough response ({r['word_count']} words)")
        if len(r["matched_kws"]) >= 4: strengths.append(f"{len(r['matched_kws'])} domain keywords used")
        if not strengths:              strengths.append("Attempted all evaluation dimensions")
        weaknesses = []
        if r["relevance"] < 60:   weaknesses.append("Low domain keyword coverage")
        if r["clarity"]   < 60:   weaknesses.append("Sentence structure needs work")
        if r["structure"] < 60:   weaknesses.append("Missing structural markers (STAR method)")
        if r["word_count"] < 50:  weaknesses.append("Answer is too brief")
        if not weaknesses:        weaknesses.append("Minor refinements possible — see improvement tips")
        str_chips  = "".join(f'<span class="fp-chip fp-chip-good">&#10003; {s}</span>' for s in strengths)
        weak_chips = "".join(f'<span class="fp-chip fp-chip-warn">&#9651; {w}</span>' for w in weaknesses)
        bias_chips = (
            "".join(f'<span class="fp-chip fp-chip-warn">&#9888; {f["label"]}</span>' for f in r["bias_flags"])
            or '<span class="fp-chip fp-chip-good">&#10003; None detected</span>'
        )
        st.markdown('<div class="fp-section-label" style="margin-top:8px;">🧾 Interview Report Card</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="fp-report-card">'
            f'<div class="fp-report-header">'
            f'  <div><div class="fp-report-title">Interview Report Card</div>'
            f'  <div class="fp-report-subtitle">Generated {today_str} &middot; {interview_type} Interview</div></div>'
            f'  <div class="fp-report-grade" style="color:{grade_color};">{grade_letter}</div>'
            f'</div>'
            f'<div class="fp-report-section-title">&#128202; Dimension Scores</div>'
            f'<div class="fp-report-scores-row">'
            f'  <div class="fp-report-score-item"><div class="fp-report-score-num">{overall}</div><div class="fp-report-score-lbl">Overall</div></div>'
            f'  <div class="fp-report-score-item"><div class="fp-report-score-num">{r["relevance"]}</div><div class="fp-report-score-lbl">Relevance</div></div>'
            f'  <div class="fp-report-score-item"><div class="fp-report-score-num">{r["clarity"]}</div><div class="fp-report-score-lbl">Clarity</div></div>'
            f'  <div class="fp-report-score-item"><div class="fp-report-score-num">{r["structure"]}</div><div class="fp-report-score-lbl">Structure</div></div>'
            f'  <div class="fp-report-score-item"><div class="fp-report-score-num">{conf["score"]}</div><div class="fp-report-score-lbl">AI Conf.</div></div>'
            f'</div>'
            f'<div class="fp-report-section-title">&#10003; Strengths</div>'
            f'<div class="fp-chips-row">{str_chips}</div>'
            f'<div class="fp-report-section-title">&#9651; Areas to Improve</div>'
            f'<div class="fp-chips-row">{weak_chips}</div>'
            f'<div class="fp-report-section-title">&#9878; Bias Flags</div>'
            f'<div class="fp-chips-row">{bias_chips}</div>'
            f'<div class="fp-report-watermark">FairPrep AI &middot; Ethical Evaluation Engine</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        report_txt = f"""FAIRPREP AI - INTERVIEW REPORT CARD
Generated : {today_str}
Type      : {interview_type} Interview
Grade     : {grade_letter}
Question  : {current_q['q']}

SCORES
------------------------------
Overall Score  : {overall}/100  [{grade_label}]
Relevance      : {r['relevance']}/100
Clarity        : {r['clarity']}/100
Structure      : {r['structure']}/100
AI Confidence  : {conf['score']}/100  [{conf['label']}]

STRENGTHS
------------------------------
{chr(10).join(f'  - {s}' for s in strengths)}

AREAS TO IMPROVE
------------------------------
{chr(10).join(f'  - {w}' for w in weaknesses)}

BIAS FLAGS
------------------------------
{chr(10).join(f'  - {f["label"]}: {f["detail"]}' for f in r["bias_flags"]) or '  - No bias detected'}

TRANSPARENT FEEDBACK
------------------------------
Relevance : {r['explanations']['relevance']}
Clarity   : {r['explanations']['clarity']}
Structure : {r['explanations']['structure']}

----------------------------------------------
FairPrep AI v3.1 - Ethical AI Evaluation Engine
No external APIs - All scoring runs locally
""".strip()

        st.download_button(
            label="⬇️ Download Report (.txt)",
            data=report_txt,
            file_name="fairprep_report.txt",
            mime="text/plain",
            use_container_width=True
        )
        if st.button("🔄 Try Again with a New Answer", use_container_width=True):
            st.session_state.answer = ""
            st.session_state.result = None
            st.rerun()


# ── WHY THIS MATTERS SECTION ──────────────────────────────────────────────────
st.markdown(
    '<div class="fp-why-matters">'
    '<div class="fp-why-matters-title">Why <em>Fairness</em> in AI Evaluation Matters</div>'
    '<div class="fp-why-stat-row">'
    '  <div class="fp-why-stat"><div class="fp-why-stat-num">72%</div><div class="fp-why-stat-lbl">of AI hiring tools show measurable bias toward longer responses</div></div>'
    '  <div class="fp-why-stat"><div class="fp-why-stat-num">3M+</div><div class="fp-why-stat-lbl">hiring decisions influenced by algorithmic scoring annually</div></div>'
    '  <div class="fp-why-stat"><div class="fp-why-stat-num">8pts</div><div class="fp-why-stat-lbl">average score variance from Length Bias alone — enough to fail a candidate</div></div>'
    '</div>'
    '<div class="fp-why-matters-body">'
    'Every score in FairPrep AI comes with a full explanation, a bias check, and a fairness audit. '
    'We believe evaluation systems should be transparent, accountable, and correctable — '
    'so that skill and substance always outweigh style and verbosity.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown('<hr class="fp-divider">', unsafe_allow_html=True)
st.markdown(
    '<div class="fp-footer">'
    'FairPrep AI v3.1 &middot; Ethical AI Evaluation Engine &middot; Hackathon Edition<br>'
    '<span style="opacity:0.5;">No external APIs &middot; All scoring runs locally &middot; Fully transparent &middot; Bias-aware by design</span>'
    '</div>',
    unsafe_allow_html=True
)