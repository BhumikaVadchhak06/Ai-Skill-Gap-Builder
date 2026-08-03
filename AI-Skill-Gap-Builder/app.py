import streamlit as st
from pathlib import Path

from resume_parser import extract_resume_text
from resume_validator import is_resume
from skill_analyzer import (
    extract_skills,
    analyze_resume
)

from roadmap_generator import generate_roadmap

import json

# ── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Skill Gap Builder — Career Compass AI",
    page_icon="⚡",
    layout="centered"
)

# ── SVG Icon Library ─────────────────────────────────────────────────────

SVG_TARGET = '<svg class="icon icon-target" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M32 4a28 28 0 0 1 28 28" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/><path d="M60 32a28 28 0 0 1-28 28" stroke="#6366f1" stroke-width="3.5" stroke-linecap="round"/><path d="M4 32A28 28 0 0 1 32 4" stroke="#4f46e5" stroke-width="3.5" stroke-linecap="round"/><path d="M32 60A28 28 0 0 1 4 32" stroke="#8b5cf6" stroke-width="3.5" stroke-linecap="round"/><rect x="20" y="38" width="5" height="12" rx="1.5" fill="#6366f1"/><rect x="29" y="30" width="5" height="20" rx="1.5" fill="#3b82f6"/><rect x="38" y="22" width="5" height="28" rx="1.5" fill="#10b981"/><path d="M18 40 31 28l8 6 12-14" stroke="#1e1b4b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><polygon points="51,20 53,27 46,25" fill="#10b981"/><circle cx="12" cy="44" r="2.5" fill="#6366f1"/><circle cx="8" cy="38" r="1.8" fill="#3b82f6"/><circle cx="14" cy="50" r="1.8" fill="#3b82f6"/><line x1="12" y1="44" x2="8" y2="38" stroke="#6366f1" stroke-width="1.2"/><line x1="12" y1="44" x2="14" y2="50" stroke="#6366f1" stroke-width="1.2"/><text x="22" y="20" font-family="Plus Jakarta Sans, Inter, sans-serif" font-size="14" font-weight="800" fill="#6366f1">AI</text></svg>'

SVG_ROCKET = '<svg class="icon icon-rocket" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>'

SVG_CHART = '<svg class="icon icon-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="12" width="4" height="9" rx="1.5"/><rect x="10" y="7" width="4" height="14" rx="1.5"/><rect x="17" y="3" width="4" height="18" rx="1.5"/></svg>'

SVG_CHECK = '<svg class="icon icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 12l2.5 2.5L16 9"/></svg>'

SVG_ALERT = '<svg class="icon icon-alert" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>'

SVG_PIN = '<svg class="icon icon-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>'

SVG_CALENDAR = '<svg class="icon icon-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2.5"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'

SVG_TROPHY = '<svg class="icon icon-trophy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>'

SVG_GUIDE = '<svg class="icon icon-guide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>'

SVG_WARN = '<svg class="icon icon-warn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'


# ── Helper ───────────────────────────────────────────────────────────────
def _icon(svg, extra_cls="", style=""):
    import re
    m = re.search(r'class="([^"]*)"', svg)
    if m:
        base = m.group(1)
        new_cls = base + (" " + extra_cls if extra_cls else "")
        return svg.replace(f'class="{base}"', f'class="{new_cls}"' + (f' style="{style}"' if style else ''))
    return svg


# ── Global Animated Premium Stylesheet ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { 
    font-family: 'Plus Jakarta Sans', sans-serif !important; 
}

/* ── Dynamic Animated Gradient Mesh Background ── */
.stApp {
    background: #0f172a;
    background-image: 
        radial-gradient(at 10% 10%, rgba(99, 102, 241, 0.25) 0px, transparent 50%),
        radial-gradient(at 90% 15%, rgba(168, 85, 247, 0.22) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(16, 185, 129, 0.15) 0px, transparent 50%),
        radial-gradient(at 80% 90%, rgba(236, 72, 153, 0.2) 0px, transparent 50%),
        radial-gradient(at 15% 85%, rgba(59, 130, 246, 0.22) 0px, transparent 50%);
    background-size: 140% 140%;
    animation: gradientMesh 12s ease-in-out infinite alternate;
    background-attachment: fixed;
    color: #f8fafc;
}

@keyframes gradientMesh {
    0%   { background-position: 0% 0%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 100%; }
}

/* Hide Streamlit headers */
header[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
    max-width: 880px !important;
}

/* ── Glassmorphism Color Variables ─────────────── */
:root {
    --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    --accent-glow: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #d946ef 100%);
    --card-glass: rgba(15, 23, 42, 0.65);
    --card-border: rgba(255, 255, 255, 0.12);
    --card-border-glow: rgba(99, 102, 241, 0.4);
    --shadow-glass: 0 16px 40px 0 rgba(0, 0, 0, 0.37);
}

/* ── Glassmorphic Animated Cards ──────────────── */
.card {
    background: var(--card-glass);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 22px;
    box-shadow: var(--shadow-glass);
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.card:hover {
    transform: translateY(-4px);
    border-color: var(--card-border-glow);
    box-shadow: 0 20px 48px -8px rgba(99, 102, 241, 0.3);
}

/* Shimmer line on top of cards */
.card::after {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: shimmerLine 6s ease-in-out infinite;
}

@keyframes shimmerLine {
    0%   { left: -100%; }
    50%, 100% { left: 100%; }
}

/* ── Hero Section Card ─────────────────────────── */
.hero-card {
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 30px;
    padding: 46px 36px;
    text-align: center;
    box-shadow: 0 24px 60px -12px rgba(99, 102, 241, 0.25);
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--accent-gradient);
    background-size: 200% 200%;
    animation: gradientShift 4s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── SVG Icons & Animations ────────────────────── */
.icon {
    width: 26px;
    height: 26px;
    display: inline-block;
    vertical-align: middle;
}

.icon-lg  { width: 40px; height: 40px; }
.icon-xl  { width: 56px; height: 56px; }
.icon-xxl { width: 72px; height: 72px; }

/* AI Glow Icon Animation */
.icon-target {
    animation: aiPulseGlow 3s ease-in-out infinite;
}

@keyframes aiPulseGlow {
    0%, 100% { 
        filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.4)) drop-shadow(0 0 20px rgba(168, 85, 247, 0.3));
        transform: scale(1) rotate(0deg); 
    }
    50% { 
        filter: drop-shadow(0 0 22px rgba(168, 85, 247, 0.7)) drop-shadow(0 0 35px rgba(236, 72, 153, 0.5));
        transform: scale(1.06) rotate(2deg); 
    }
}

/* Float for rocket */
.icon-rocket {
    animation: floatRocket 3.2s ease-in-out infinite;
}

@keyframes floatRocket {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50%      { transform: translateY(-7px) rotate(-4deg); }
}

/* ── Keyframe Animations ───────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}

.fade-up      { animation: fadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) both; }
.fade-up-d1   { animation: fadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.09s both; }
.fade-up-d2   { animation: fadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both; }
.fade-up-d3   { animation: fadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.27s both; }
.fade-up-d4   { animation: fadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.36s both; }

/* ── Animated Gradient Text ────────────────────── */
.grad-text {
    background: var(--accent-gradient);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: textFlow 5s linear infinite;
    font-family: 'Outfit', sans-serif !important;
}

@keyframes textFlow {
    to { background-position: 200% center; }
}

/* ── Glowing Brand Badge ───────────────────────── */
.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 20px;
    border-radius: 100px;
    background: rgba(99, 102, 241, 0.14);
    border: 1px solid rgba(168, 85, 247, 0.35);
    color: #c084fc;
    font-size: 15px;
    font-weight: 700;
    margin: 16px 0 18px 0;
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
}

/* ── Selectbox Styling ─────────────────────────── */
.stSelectbox > label,
.stFileUploader > label {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    margin-bottom: 8px !important;
}

div[data-baseweb="select"] > div {
    background: rgba(30, 41, 59, 0.8) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
    transition: all 0.25s ease !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #818cf8 !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
}

/* ── File Uploader Dropzone ───────────────────── */
[data-testid="stFileUploader"] {
    margin-top: 8px !important;
    margin-bottom: 24px !important;
}

/* Outer dropzone — compact layout */
[data-testid="stFileUploaderDropzone"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0 !important;
    padding: 18px 24px !important;
    border: 2px dashed rgba(168, 85, 247, 0.4) !important;
    border-radius: 18px !important;
    background: rgba(30, 41, 59, 0.6) !important;
    position: relative !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #c084fc !important;
    background: rgba(49, 46, 129, 0.4) !important;
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.3) !important;
}

/* Hide internal labels inside dropzone */
[data-testid="stFileUploaderDropzone"] label {
    display: none !important;
}

/* Hide ALL buttons inside dropzone (removes duplicates) */
[data-testid="stFileUploaderDropzone"] button {
    display: none !important;
}

/* Native file input */
[data-testid="stFileUploaderDropzone"] input[type="file"] {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
    z-index: 3 !important;
}

/* Hide default dropzone content */
[data-testid="stFileUploaderDropzoneInstructions"] {
    position: relative !important;
    z-index: 1 !important;
    pointer-events: none !important;
    text-align: center !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] svg,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

/* "Upload" pill button */
[data-testid="stFileUploaderDropzoneInstructions"]::before {
    content: "📄  Upload";
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 38px;
    font-size: 15px;
    font-weight: 700;
    background: var(--accent-glow);
    color: white;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.45);
    letter-spacing: 0.02em;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

[data-testid="stFileUploaderDropzone"]:hover [data-testid="stFileUploaderDropzoneInstructions"]::before {
    transform: scale(1.05);
    box-shadow: 0 8px 28px rgba(168, 85, 247, 0.6);
}

/* Uploaded file parent overflow fix */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] > div > div {
    overflow: visible !important;
}

/* Uploaded file card */
[data-testid="stFileUploaderFile"] {
    position: relative !important;
    overflow: visible !important;
    margin-top: 12px !important;
    background: rgba(30, 41, 59, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    color: #ffffff !important;
}

/* Cross button — top-right corner */
[data-testid="stFileUploaderFile"] button {
    display: flex !important;
    position: absolute !important;
    top: -10px !important;
    right: -10px !important;
    width: 26px !important;
    height: 26px !important;
    min-width: 26px !important;
    min-height: 26px !important;
    max-width: 26px !important;
    max-height: 26px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    background: #64748b !important;
    border: 2.5px solid #0f172a !important;
    color: #fff !important;
    font-size: 13px !important;
    line-height: 1 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4) !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    z-index: 10 !important;
    transition: background 0.2s ease, transform 0.2s ease !important;
}

[data-testid="stFileUploaderFile"] button:hover {
    background: #ef4444 !important;
    transform: scale(1.18) !important;
}

[data-testid="stFileUploaderFile"] button span {
    font-size: 0 !important;
}

[data-testid="stFileUploaderFile"] button svg {
    width: 14px !important;
    height: 14px !important;
    stroke: white !important;
}

/* ── Metric Cards ──────────────────────────────── */
.metric-card {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    padding: 24px 18px;
    text-align: center;
    box-shadow: var(--shadow-glass);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.metric-card:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: rgba(168, 85, 247, 0.4);
    box-shadow: 0 16px 36px rgba(99, 102, 241, 0.25);
}

.metric-val {
    font-size: 38px;
    font-weight: 800;
    margin: 8px 0 2px 0;
    font-family: 'Outfit', sans-serif !important;
}

.metric-label {
    font-size: 12px;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Animated Glowing Progress Bar ─────────────── */
.progress-track {
    width: 100%;
    height: 24px;
    background: rgba(30, 41, 59, 0.8);
    border-radius: 20px;
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.5);
}

.progress-bar {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899, #10b981);
    background-size: 300% 100%;
    animation: liquidMove 4s ease infinite;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 18px rgba(168, 85, 247, 0.6);
}

@keyframes liquidMove {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.progress-pct {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-weight: 800;
    font-size: 12px;
    color: #ffffff;
    text-shadow: 0 1px 4px rgba(0,0,0,0.6);
}

/* ── Glowing Skill Pills ───────────────────────── */
.pill {
    display: inline-flex;
    align-items: center;
    padding: 7px 18px;
    margin: 4px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    background: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    transition: all 0.25s ease;
}

.pill:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
    background: rgba(99, 102, 241, 0.25);
}

.pill-matched {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border-color: rgba(16, 185, 129, 0.35);
}

.pill-matched:hover {
    box-shadow: 0 0 16px rgba(16, 185, 129, 0.45);
    background: rgba(16, 185, 129, 0.25);
}

.pill-missing {
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border-color: rgba(239, 68, 68, 0.35);
}

.pill-missing:hover {
    box-shadow: 0 0 16px rgba(239, 68, 68, 0.45);
    background: rgba(239, 68, 68, 0.25);
}

/* ── Neon Roadmap Card ─────────────────────────── */
.roadmap-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-left: 4px solid #a855f7;
    border-radius: 0 18px 18px 0;
    padding: 18px 22px;
    margin-bottom: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.roadmap-card:hover {
    transform: translateX(8px);
    border-left-color: #ec4899;
    box-shadow: 0 0 24px rgba(168, 85, 247, 0.3);
}

.week-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 700;
    background: rgba(168, 85, 247, 0.2);
    color: #e9d5ff;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

/* ── Guide Steps ───────────────────────────────── */
.guide-step {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 16px;
    margin-bottom: 10px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-left: 4px solid #ec4899;
    transition: all 0.25s ease;
}

.guide-step:hover {
    transform: translateX(6px);
    background: rgba(51, 65, 85, 0.8);
    box-shadow: 0 0 20px rgba(236, 72, 153, 0.25);
}

.guide-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 14px;
    background: var(--accent-glow);
    color: #ffffff;
    flex-shrink: 0;
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
}

/* ── Section Header ────────────────────────────── */
.section-hdr {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 18px 0;
}

.section-hdr h3 {
    margin: 0;
    font-weight: 800;
    font-size: 22px;
    color: #ffffff;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Celebration Card ──────────────────────────── */
.celebration-card {
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(245, 158, 11, 0.25));
    border: 1px solid rgba(251, 191, 36, 0.4);
    text-align: center;
    padding: 38px 28px;
    border-radius: 26px;
    box-shadow: 0 0 35px rgba(245, 158, 11, 0.25);
}

/* ── Streamlit Success & Alert Boxes ──────────── */
[data-testid="stAlert"] {
    background: rgba(15, 23, 42, 0.85) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(16, 185, 129, 0.4) !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(16, 185, 129, 0.15) !important;
    padding: 14px 20px !important;
}

[data-testid="stAlert"] div,
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #4ade80 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

/* ── Divider ───────────────────────────────────── */
.divider {
    width: 70px;
    height: 4px;
    background: var(--accent-gradient);
    border-radius: 4px;
    margin: 16px auto;
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
}

</style>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────────────
_target_hero = _icon(SVG_TARGET, "icon-xxl", "color:#818cf8;")
_rocket_hero = _icon(SVG_ROCKET, "icon-lg", "color:#c084fc;")

st.markdown(f"""<div class="hero-card fade-up">
<div style="margin-bottom:14px;" class="fade-up-d1">{_target_hero}</div>
<h1 class="grad-text fade-up-d2" style="font-size:46px; font-weight:800; margin:0 0 6px 0; line-height:1.15; letter-spacing:-0.02em;">AI Skill Gap Builder</h1>
<div class="divider fade-up-d2"></div>
<div class="brand-badge fade-up-d3">{_rocket_hero}<span>Career Compass AI</span></div>
<p class="fade-up-d4" style="font-size:15px; color:#cbd5e1; margin:0; line-height:1.7;">Analyze Resume &nbsp;&middot;&nbsp; Find Skill Gaps &nbsp;&middot;&nbsp; AI Roadmap &nbsp;&middot;&nbsp; Job Readiness<br/><span style="font-size:13px; color:#94a3b8;">Upload your resume and receive personalized career guidance powered by AI.</span></p>
</div>""", unsafe_allow_html=True)


# ── Career Goal & Upload ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
CAREER_DATA_PATH = BASE_DIR / "data" / "career_skills.json"

with CAREER_DATA_PATH.open("r", encoding="utf-8") as f:
    career_data = json.load(f)

goal = st.selectbox(
    "Select Career Goal",
    list(career_data.keys())
)

resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if resume:

    text = extract_resume_text(resume)

    if not is_resume(text):
        st.error("❌ Wrong file uploaded. Please upload a valid Resume PDF.")
        st.stop()

    st.success("✅ Resume Uploaded Successfully")
    print(text)

    detected_skills = extract_skills(text)

    score, matched, missing = analyze_resume(
        goal,
        detected_skills
    )

    # ── Metric Cards ─────────────────────────────────────────────────
    _chart_lg = _icon(SVG_CHART, "icon-lg", "color:#818cf8;")
    _check_lg = _icon(SVG_CHECK, "icon-lg", "color:#34d399;")
    _alert_lg = _icon(SVG_ALERT, "icon-lg", "color:#f87171;")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""<div class="metric-card fade-up-d1">
{_chart_lg}
<div class="metric-val grad-text">{score}%</div>
<div class="metric-label">Match Score</div>
</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="metric-card fade-up-d2">
{_check_lg}
<div class="metric-val" style="color:#34d399;">{len(detected_skills)}</div>
<div class="metric-label">Skills Found</div>
</div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div class="metric-card fade-up-d3">
{_alert_lg}
<div class="metric-val" style="color:#f87171;">{len(missing)}</div>
<div class="metric-label">Missing Skills</div>
</div>""", unsafe_allow_html=True)

    # ── Progress Bar ─────────────────────────────────────────────────
    _chart_sm = _icon(SVG_CHART, "", "color:#818cf8;")
    st.markdown(f"""<div class="section-hdr fade-up-d1">
{_chart_sm}
<h3>Resume Match Score</h3>
</div>
<div class="progress-track fade-up-d2">
<div class="progress-bar" style="width:{score}%;"></div>
<div class="progress-pct">{score}%</div>
</div>""", unsafe_allow_html=True)

    # ── Detected Skills ──────────────────────────────────────────────
    skills_pills = "".join(
        [f'<span class="pill">{s}</span>' for s in detected_skills]
    )
    _pin_lg = _icon(SVG_PIN, "icon-lg", "color:#818cf8;")
    st.markdown(f"""<div class="card fade-up-d3" style="margin-top:24px;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
{_pin_lg}
<h3 style="margin:0; font-weight:800; font-size:18px; color:#ffffff;">Detected Skills</h3>
</div>
<div>{skills_pills}</div>
</div>""", unsafe_allow_html=True)

    # ── Matched / Missing Skills ─────────────────────────────────────
    matched_pills = "".join(
        [f'<span class="pill pill-matched">{s}</span>' for s in matched]
    )
    missing_pills = "".join(
        [f'<span class="pill pill-missing">{s}</span>' for s in missing]
    )

    _check_sm = _icon(SVG_CHECK, "", "color:#34d399;")
    _alert_sm = _icon(SVG_ALERT, "", "color:#f87171;")

    mcol1, mcol2 = st.columns(2)

    with mcol1:
        mp = matched_pills if matched_pills else '<span style="color:#94a3b8; font-size:13px;">None yet</span>'
        st.markdown(f"""<div class="card fade-up-d3" style="border-left:4px solid #10b981;">
<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
{_check_sm}
<h3 style="margin:0; font-weight:800; font-size:16px; color:#34d399;">Matched Skills</h3>
</div>
<div>{mp}</div>
</div>""", unsafe_allow_html=True)

    with mcol2:
        ms = missing_pills if missing_pills else '<span style="color:#94a3b8; font-size:13px;">All clear!</span>'
        st.markdown(f"""<div class="card fade-up-d4" style="border-left:4px solid #ef4444;">
<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
{_alert_sm}
<h3 style="margin:0; font-weight:800; font-size:16px; color:#f87171;">Missing Skills</h3>
</div>
<div>{ms}</div>
</div>""", unsafe_allow_html=True)

    # ── Roadmap ──────────────────────────────────────────────────────
    roadmap = generate_roadmap(missing)

    _cal_lg = _icon(SVG_CALENDAR, "icon-lg", "color:#c084fc;")
    _cal_sm = _icon(SVG_CALENDAR, "", "width:14px;height:14px;color:#c084fc;")

    st.markdown(f"""<div class="section-hdr fade-up">
{_cal_lg}
<h3>Step-by-Step Roadmap</h3>
</div>""", unsafe_allow_html=True)

    for i, step in enumerate(roadmap, start=1):
        delay = min(i * 0.07, 0.5)
        st.markdown(f"""<div class="roadmap-card" style="animation: fadeInUp 0.5s ease {delay}s both;">
<div style="display:flex; align-items:center; gap:12px;">
<span class="week-badge">{_cal_sm} Week {i}</span>
<span style="font-size:14px; color:#f1f5f9; font-weight:600;">{step}</span>
</div>
</div>""", unsafe_allow_html=True)

    # ── Job Ready or Improvement ─────────────────────────────────────
    if score >= 85:

        st.balloons()

        _trophy_xl = _icon(SVG_TROPHY, "icon-xxl", "color:#fbbf24;")
        st.markdown(f"""<div class="celebration-card fade-up" style="margin-top:28px;">
<div style="margin-bottom:12px;">{_trophy_xl}</div>
<h2 class="grad-text" style="font-size:30px; font-weight:800; margin:0 0 6px 0;">Congratulations! You are Job Ready.</h2>
<p style="color:#fef08a; font-size:15px; font-weight:600; margin:0;">Your skills align excellently with your career goal.</p>
</div>""", unsafe_allow_html=True)

        guide_steps = [
            "Update your Resume with matched skills",
            "Refresh your LinkedIn profile",
            "Upload Projects on GitHub",
            "Apply on LinkedIn Jobs",
            "Apply on Naukri / Indeed",
            "Prepare for Interviews",
            "Start Networking"
        ]

        _guide_lg = _icon(SVG_GUIDE, "icon-lg", "color:#c084fc;")
        guide_html = "".join([
            f'<div class="guide-step" style="animation: fadeInUp 0.4s ease {0.08 * idx}s both;">'
            f'<span class="guide-num">{idx + 1}</span>'
            f'<span style="font-size:14px; color:#f1f5f9; font-weight:600;">{s}</span>'
            f'</div>'
            for idx, s in enumerate(guide_steps)
        ])

        st.markdown(f"""<div class="card fade-up-d2" style="margin-top:16px;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
{_guide_lg}
<h3 style="margin:0; font-weight:800; font-size:18px; color:#ffffff;">Application Guide</h3>
</div>
{guide_html}
</div>""", unsafe_allow_html=True)

    else:
        pass
