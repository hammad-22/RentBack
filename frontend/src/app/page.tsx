"use client";

import styles from "./page.module.css";
import { useEffect, useState } from "react";
import NYCMap from "@/components/NYCMap";
import { getStats } from "@/lib/api";

const YEAR = new Date().getFullYear();

function AnimatedNumber({ target, prefix = "", suffix = "" }: { target: number; prefix?: string; suffix?: string }) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = 0;
    const duration = 2000;
    const step = (timestamp: number) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(Math.floor(eased * target));
      if (progress < 1) requestAnimationFrame(step);
    };
    const timer = setTimeout(() => requestAnimationFrame(step), 500);
    return () => clearTimeout(timer);
  }, [target]);
  return <span>{prefix}{value.toLocaleString()}{suffix}</span>;
}

export default function Home() {
  const [stats, setStats] = useState({
    avgAnnualSavings: 2847,
    avgOverpaymentRate: 14,
    neighborhoodsCovered: 8,
  });

  useEffect(() => {
    getStats()
      .then(data => setStats({
        avgAnnualSavings: data.avg_annual_savings,
        avgOverpaymentRate: data.avg_overpayment_rate,
        neighborhoodsCovered: data.neighborhoods_covered,
      }))
      .catch(() => { /* keep defaults on error */ });
  }, []);

  return (
    <main className={styles.main}>

      {/* NYC Map Background */}
      <NYCMap className={styles.mapBg} />

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className="container animate-in">
          <div className={styles.heroLayout}>
            <div className={styles.heroContent}>
              <div className={styles.preTitle}>New York City Rental Intelligence</div>
              <h1 className={styles.heroTitle}>
                Negotiate your rent with precision.
              </h1>
              <p className={styles.heroSubtitle}>
                A computational engine that analyzes local comparables, adjusts for your specific unit's amenities,
                and generates a data-backed negotiation strategy for your lease renewal.
              </p>
              <div className={styles.heroActions}>
                <a href="/analyze" className="btn btn-primary">Begin Analysis</a>
                <a href="#methodology" className="btn btn-secondary">Our Methodology</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Live Stats Ticker */}
      <section className={styles.statsSection}>
        <div className="container">
          <div className={`${styles.statsRow} animate-in delay-1`}>
            <div className={styles.stat}>
              <div className={styles.statValue}><AnimatedNumber target={stats.avgAnnualSavings} prefix="$" /></div>
              <div className={styles.statLabel}>Average Annual Savings</div>
            </div>
            <div className={styles.statDivider} />
            <div className={styles.stat}>
              <div className={styles.statValue}><AnimatedNumber target={stats.avgOverpaymentRate} suffix="%" /></div>
              <div className={styles.statLabel}>Avg. NYC Overpayment Rate</div>
            </div>
            <div className={styles.statDivider} />
            <div className={styles.stat}>
              <div className={styles.statValue}><AnimatedNumber target={stats.neighborhoodsCovered} /></div>
              <div className={styles.statLabel}>Neighborhoods Covered</div>
            </div>
            <div className={styles.statDivider} />
            <div className={styles.stat}>
              <div className={styles.statValue}>&lt;60s</div>
              <div className={styles.statLabel}>Report Generation Time</div>
            </div>
          </div>
        </div>
      </section>

      {/* Methodology Section with Visuals */}
      <section id="methodology" className={styles.methodologySection}>
        <div className="container">
          <div className={`${styles.methodHeader} animate-in delay-2`}>
            <div className={styles.preTitle}>How It Works</div>
            <h2>Three-stage analytical pipeline</h2>
          </div>

          {/* Stage 1 */}
          <div className={`${styles.methodRow} animate-in delay-2`}>
            <div className={styles.methodVisual}>
              <div className={styles.miniChart}>
                <div className={styles.chartLabel}>Comparable Radius</div>
                <svg viewBox="0 0 220 220" className={styles.chartSvg}>
                  {/* City block grid */}
                  <g stroke="currentColor" fill="none" opacity="0.2" strokeWidth="0.5">
                    {/* Horizontal streets */}
                    <line x1="10" y1="30" x2="210" y2="30" />
                    <line x1="10" y1="70" x2="210" y2="70" />
                    <line x1="10" y1="110" x2="210" y2="110" />
                    <line x1="10" y1="150" x2="210" y2="150" />
                    <line x1="10" y1="190" x2="210" y2="190" />
                    {/* Vertical streets */}
                    <line x1="20" y1="20" x2="20" y2="200" />
                    <line x1="65" y1="20" x2="65" y2="200" />
                    <line x1="110" y1="20" x2="110" y2="200" />
                    <line x1="155" y1="20" x2="155" y2="200" />
                    <line x1="200" y1="20" x2="200" y2="200" />
                  </g>
                  {/* Block fills (buildings) */}
                  <g fill="currentColor" opacity="0.06">
                    <rect x="24" y="34" width="37" height="32" rx="1" />
                    <rect x="69" y="34" width="37" height="32" rx="1" />
                    <rect x="114" y="34" width="37" height="32" rx="1" />
                    <rect x="159" y="34" width="37" height="32" rx="1" />
                    <rect x="24" y="74" width="37" height="32" rx="1" />
                    <rect x="69" y="74" width="37" height="32" rx="1" />
                    <rect x="114" y="74" width="37" height="32" rx="1" />
                    <rect x="159" y="74" width="37" height="32" rx="1" />
                    <rect x="24" y="114" width="37" height="32" rx="1" />
                    <rect x="69" y="114" width="37" height="32" rx="1" />
                    <rect x="114" y="114" width="37" height="32" rx="1" />
                    <rect x="159" y="114" width="37" height="32" rx="1" />
                    <rect x="24" y="154" width="37" height="32" rx="1" />
                    <rect x="69" y="154" width="37" height="32" rx="1" />
                    <rect x="114" y="154" width="37" height="32" rx="1" />
                    <rect x="159" y="154" width="37" height="32" rx="1" />
                  </g>
                  {/* Your location — center pin */}
                  <g transform="translate(110, 110)">
                    <path d="M0,-12 C-4,-12 -7,-9 -7,-5 C-7,0 0,8 0,8 C0,8 7,0 7,-5 C7,-9 4,-12 0,-12 Z" fill="currentColor" />
                    <circle cx="0" cy="-5" r="2.5" fill="var(--bg-primary)" />
                  </g>
                  {/* Comparable pins */}
                  {[
                    [42, 50], [87, 90], [132, 50], [175, 130],
                    [42, 130], [87, 170], [175, 90], [42, 170],
                  ].map(([cx, cy], i) => (
                    <g key={i} transform={`translate(${cx}, ${cy})`} opacity={i < 5 ? 0.6 : 0.3}>
                      <path d="M0,-8 C-3,-8 -5,-6 -5,-3.5 C-5,0 0,5 0,5 C0,5 5,0 5,-3.5 C5,-6 3,-8 0,-8 Z" fill="currentColor" />
                      <circle cx="0" cy="-3.5" r="1.5" fill="var(--bg-primary)" />
                    </g>
                  ))}
                  {/* Radius indicator */}
                  <circle cx="110" cy="110" r="90" fill="none" stroke="currentColor" strokeWidth="0.5" strokeDasharray="4 3" opacity="0.2" />
                  <text x="110" y="215" textAnchor="middle" fontSize="7" fill="currentColor" opacity="0.4" fontFamily="Inter, sans-serif">0.5 mi radius</text>
                </svg>
              </div>
            </div>
            <div className={styles.methodText}>
              <div className={styles.methodNumber}>01</div>
              <h3>Hyper-Local Data Collection</h3>
              <p>
                We aggregate active rental listings within a precise 0.5-mile radius of your address.
                Data is sourced from StreetEasy, Zillow, and Apartments.com to ensure comprehensive coverage
                of the NYC market landscape.
              </p>
            </div>
          </div>

          {/* Stage 2 */}
          <div className={`${styles.methodRow} ${styles.methodRowReverse} animate-in delay-3`}>
            <div className={styles.methodVisual}>
              <div className={styles.miniChart}>
                <div className={styles.chartLabel}>Feature Adjustment Engine</div>
                <div className={styles.adjustmentBars}>
                  {[
                    { label: "Sq ft delta", value: -276, pct: 40 },
                    { label: "Floor level", value: -210, pct: 30 },
                    { label: "In-unit laundry", value: -100, pct: 15 },
                    { label: "Doorman", value: +150, pct: 22, positive: true },
                    { label: "Elevator", value: +40, pct: 6, positive: true },
                  ].map((adj, i) => (
                    <div key={i} className={styles.adjBar}>
                      <div className={styles.adjLabel}>{adj.label}</div>
                      <div className={styles.adjTrack}>
                        <div
                          className={`${styles.adjFill} ${adj.positive ? styles.adjPositive : styles.adjNegative}`}
                          style={{ width: `${adj.pct}%` }}
                        />
                      </div>
                      <div className={styles.adjValue}>{adj.positive ? "+" : ""}{adj.value}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className={styles.methodText}>
              <div className={styles.methodNumber}>02</div>
              <h3>Algorithmic Rent Adjustment</h3>
              <p>
                Raw comparisons are misleading. A 5th-floor doorman building shouldn't be directly compared to
                a walk-up. Our engine applies per-feature regression weights — adjusting each comparable's rent
                for differences in square footage, floor level, laundry access, and 15+ other variables.
              </p>
            </div>
          </div>

          {/* Stage 3 */}
          <div className={`${styles.methodRow} animate-in delay-3`}>
            <div className={styles.methodVisual}>
              <div className={styles.miniChart}>
                <div className={styles.chartLabel}>Output: Negotiation Portfolio</div>
                <div className={styles.outputPreview}>
                  <div className={styles.outputLine}>
                    <span className={styles.outputDot} /> Market Analysis Report
                  </div>
                  <div className={styles.outputLine}>
                    <span className={styles.outputDot} /> Adjusted Comparable Grid
                  </div>
                  <div className={styles.outputLine}>
                    <span className={styles.outputDot} /> AI-Drafted Negotiation Letter
                  </div>
                  <div className={styles.outputLine}>
                    <span className={styles.outputDot} /> Timing & Leverage Advisory
                  </div>
                  <div className={styles.outputSample}>
                    <em>"Based on 12 comparable units, your current rent of $3,500 exceeds the adjusted market rate of $3,050 by 14.8%..."</em>
                  </div>
                </div>
              </div>
            </div>
            <div className={styles.methodText}>
              <div className={styles.methodNumber}>03</div>
              <h3>Strategy Generation</h3>
              <p>
                Your results include a comprehensive market brief, a sortable table of adjusted comparables,
                and a professionally drafted email to your landlord — powered by large language models and packed
                with hard data points specific to your unit.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Footer */}
      <section className={styles.ctaSection}>
        <div className="container" style={{ textAlign: "center" }}>
          <h2>Stop guessing. Start negotiating.</h2>
          <p className="text-muted" style={{ maxWidth: 500, margin: "1rem auto 2.5rem", fontSize: "1.1rem" }}>
            Join thousands of NYC renters who have used data to take control of their lease renewal.
          </p>
          <a href="/analyze" className="btn btn-primary">
            Analyze My Rent — Free
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className="container">
          <div className={styles.footerInner}>
            <span style={{ fontFamily: "var(--font-serif)", fontSize: "1.25rem", fontWeight: 600 }}>RentBack</span>
            <span className="text-muted" style={{ fontSize: "0.85rem" }}>© {YEAR} · Built for New York City renters</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
