"""Inline SVG icon sprite: 24×24 line icons, stroke = currentColor. Use kit.icon(name)."""

_P = {
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.8 2.9-6 6.5-6s6.5 2.2 6.5 6"/><circle cx="17" cy="7" r="2.8"/><path d="M16 13.2c3.3 0 5.5 2 5.5 5.3"/>',
    'doctor': '<circle cx="12" cy="7" r="3.8"/><path d="M4.5 21c0-4.2 3.3-6.8 7.5-6.8s7.5 2.6 7.5 6.8"/><path d="M9 14.6v3.2a2 2 0 0 0 4 0"/><circle cx="16" cy="18" r="1.4"/><path d="M15 14.6v2"/>',
    'nurse': '<path d="M7 6.5 12 4l5 2.5V9H7z"/><path d="M12 5.4v2.2M10.9 6.5h2.2"/><circle cx="12" cy="12" r="3"/><path d="M5 21c0-3.6 3.1-5.8 7-5.8s7 2.2 7 5.8"/>',
    'clipboard': '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9zM8.5 11h7M8.5 14.5h7M8.5 18h4"/>',
    'file': '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 15.5h6M9 19h4"/>',
    'pdf': '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M8.5 16.5v-4h1.4a1.2 1.2 0 0 1 0 2.4H8.5M12.5 12.5v4h1a1.8 1.8 0 0 0 0-4zM16 16.5v-4h1.8M16 14.6h1.4"/>',
    'folder': '<path d="M3 6.5h6l2 2.2h10V19H3z"/>',
    'mail': '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 7 8.5 6.5L20.5 7"/>',
    'phone': '<path d="M6.5 3.5h3l1.5 4-2 1.3a10 10 0 0 0 6.2 6.2l1.3-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2z"/>',
    'calendar': '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/><path d="M7.5 13h2M11 13h2M14.5 13h2M7.5 16.5h2M11 16.5h2"/>',
    'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5.2l3.4 2"/>',
    'hourglass': '<path d="M7 3h10M7 21h10M8 3c0 5 8 5 8 9s-8 4-8 9M16 3c0 5-8 5-8 9s8 4 8 9"/>',
    'syringe': '<path d="m18 3 3 3M19.5 4.5l-3 3M16.5 7.5l-9 9-2.5.5.5-2.5 9-9zM13 6l5 5M5 19l-2 2M9.5 11.5l1.5 1.5M11.5 9.5 13 11"/>',
    'spray': '<path d="M9 9h6v12H9z"/><path d="M10 9V6.5h4V9M11 6.5V4h2v2.5"/><path d="M16.5 4.5h1.5M17 2.5l1.3-.8M17 6.5l1.3.8"/>',
    'diary': '<path d="M6 3.5h11a2 2 0 0 1 2 2v15H8a2 2 0 0 1-2-2z"/><path d="M6 18.5a2 2 0 0 1 2-2h11M10 7.5h6M10 11h4"/>',
    'scope': '<path d="M3 20c3-1 4-3 5.5-6.5L11 8"/><circle cx="12.5" cy="6.2" r="2.6"/><path d="m14.6 7.8 5.4 5.4M17 12.5l2.2-2.2"/>',
    'ct': '<circle cx="12" cy="11" r="7.5"/><circle cx="12" cy="11" r="3"/><path d="M3 20.5h18M7 20.5l1-3M17 20.5l-1-3"/>',
    'tube': '<path d="M9 3h6M10 3v14a2 2 0 0 0 4 0V3"/><path d="M10 12h4"/><path d="M10 15h4" opacity=".5"/>',
    'ecg': '<path d="M2.5 12h4l2-5 3 10 2.5-7 1.5 2h6"/>',
    'lungs': '<path d="M12 3v8M12 11c-1.5 0-2.5-1-3.5-2.5C6 6 3 8 3 13c0 4 1 7 3.5 7 2.2 0 3.5-1.6 3.5-4v-3M12 11c1.5 0 2.5-1 3.5-2.5C18 6 21 8 21 13c0 4-1 7-3.5 7-2.2 0-3.5-1.6-3.5-4v-3"/>',
    'nose': '<path d="M11 3c0 4-3.5 9-3.5 12.5A3 3 0 0 0 10.5 19h3a3 3 0 0 0 3-3"/><path d="M9.5 16.5c.6.7 1.4 1 2.3 1"/><path d="M17.5 7c1 .6 1.7 1.6 2 2.8M18.5 4.5c1.6 1 2.7 2.7 3 4.6"/>',
    'list': '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3.5 6 1 1 2-2M3.5 12l1 1 2-2M3.5 18l1 1 2-2"/>',
    'scale': '<rect x="3.5" y="4" width="17" height="16" rx="3"/><path d="M8 9a5 5 0 0 1 8 0M12 9l1.5-2"/>',
    'flask': '<path d="M9.5 3h5M10.5 3v6L5 19a1.5 1.5 0 0 0 1.3 2h11.4A1.5 1.5 0 0 0 19 19l-5.5-10V3"/><path d="M7.5 15h9"/>',
    'microscope': '<path d="M9 3.5h3l1 1v5h-5v-5z"/><path d="M10.5 9.5v3M6 21h12M8 18h8M14.5 12a5 5 0 0 1 0 6"/><circle cx="10.5" cy="14" r="1.5"/>',
    'shield': '<path d="M12 3 4.5 6v5.5c0 4.5 3.2 8 7.5 9.5 4.3-1.5 7.5-5 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    'alert': '<path d="M12 3.5 2.5 20h19z"/><path d="M12 9.5v5M12 17.2v.3"/>',
    'check': '<path d="m4.5 12.5 4.5 4.5L19.5 6.5"/>',
    'x': '<path d="M6 6l12 12M18 6 6 18"/>',
    'lock': '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.3"/>',
    'key': '<circle cx="8" cy="15" r="4"/><path d="m11 12 8.5-8.5M16 7l2.5 2.5M14 9l2 2"/>',
    'hospital': '<path d="M4 21V7l8-4 8 4v14z"/><path d="M12 8v6M9 11h6M9.5 21v-3.5h5V21"/>',
    'bed': '<path d="M3 6v13M3 15h18v4M21 15v-3a3 3 0 0 0-3-3h-7v6"/><circle cx="7" cy="11.5" r="2"/>',
    'pill': '<rect x="3" y="8.5" width="18" height="7" rx="3.5" transform="rotate(-35 12 12)"/><path d="m9.6 8.4 4 5.7" />',
    'truck': '<path d="M2.5 6h11v10h-11zM13.5 9.5h4l3 3.5V16h-7z"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'snow': '<path d="M12 2.5v19M3.8 7.2l16.4 9.6M3.8 16.8l16.4-9.6M9.5 4l2.5 2 2.5-2M9.5 20l2.5-2 2.5 2"/>',
    'upload': '<path d="M7 18.5a4.5 4.5 0 0 1-.5-9A6 6 0 0 1 18 8.5a4 4 0 0 1-.5 10"/><path d="M12 11v9M9 14l3-3 3 3"/>',
    'monitor': '<rect x="3" y="4" width="18" height="12.5" rx="1.8"/><path d="M8.5 20.5h7M12 16.5v4"/>',
    'shuffle': '<path d="M3 7h3.5c4 0 6.5 10 11 10H21M3 17h3.5c1.8 0 3.2-1.7 4.4-3.8M14.5 9.2C15.6 7.9 16.6 7 18 7h3"/><path d="m18.5 4.5 2.5 2.5-2.5 2.5M18.5 14.5l2.5 2.5-2.5 2.5"/>',
    'female': '<circle cx="12" cy="9" r="5"/><path d="M12 14v7M9 18h6"/>',
    'body': '<circle cx="12" cy="4.5" r="2"/><path d="M8 8h8l-1 7h-6zM9.5 15l-.8 6.5M14.5 15l.8 6.5M8 8l-3 5M16 8l3 5"/>',
    'star': '<path d="m12 3 2.7 5.6 6.1.8-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1-4.4-4.3 6.1-.8z"/>',
    'flag': '<path d="M5 21V4M5 4.5h11l-2 4 2 4H5"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5.5 5.5"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    'drop': '<path d="M12 3.5c3 4.2 6 7.4 6 10.8a6 6 0 0 1-12 0c0-3.4 3-6.6 6-10.8z"/>',
    'bolt': '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6z"/>',
    'pause': '<rect x="6.5" y="5" width="3.5" height="14" rx="1"/><rect x="14" y="5" width="3.5" height="14" rx="1"/>',
    'stop': '<circle cx="12" cy="12" r="8.5"/><path d="M6 6l12 12"/>',
    'arrowr': '<path d="M4 12h15M14 7l5 5-5 5"/>',
    'pen': '<path d="m4 20 1-4.5L15.5 5a2 2 0 0 1 3 3L8 18.5zM13.5 7l3 3"/>',
    'eye': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    'virus': '<circle cx="12" cy="12" r="5"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
    'baby': '<circle cx="12" cy="8" r="4.5"/><path d="M10.4 7.5h.1M13.5 7.5h.1M10.5 10a2 2 0 0 0 3 0M7 21c.5-3.5 2.4-6 5-6s4.5 2.5 5 6"/>',
}


def sprite():
    syms = ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
                   f'stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in _P.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>'


NAMES = set(_P)
