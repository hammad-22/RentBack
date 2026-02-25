"use client";

// Minimalist NYC street grid background
// Renders like a zoomed-in Apple Maps / Google Maps view of a Manhattan neighborhood
export default function NYCMap({ className }: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 600 800"
            fill="none"
            stroke="currentColor"
            className={className}
            aria-hidden="true"
        >
            {/* Manhattan-angled street grid (~29° rotation like the real grid) */}
            <g transform="rotate(-29, 300, 400)" strokeWidth="0.4" opacity="0.6">
                {/* Horizontal streets */}
                {Array.from({ length: 30 }, (_, i) => (
                    <line key={`h${i}`} x1="-100" y1={i * 40 - 200} x2="800" y2={i * 40 - 200} strokeWidth="0.4" />
                ))}

                {/* Vertical avenues (wider spacing, thicker) */}
                {Array.from({ length: 12 }, (_, i) => (
                    <line key={`v${i}`} x1={i * 70 - 50} y1="-300" x2={i * 70 - 50} y2="1200" strokeWidth={i % 3 === 0 ? "0.7" : "0.35"} />
                ))}
            </g>

            {/* A diagonal cutting through — Broadway */}
            <line x1="100" y1="0" x2="500" y2="800" strokeWidth="0.6" opacity="0.4" strokeDasharray="6 4" />

            {/* Park / green space rectangle (Central Park suggestion) */}
            <rect x="220" y="180" width="80" height="180" rx="3" strokeWidth="0.6" opacity="0.3" strokeDasharray="3 3" />
        </svg>
    );
}
