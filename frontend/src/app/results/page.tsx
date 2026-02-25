"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AnalysisResponse } from "@/lib/api";
import styles from "./results.module.css";

export default function ResultsPage() {
    const router = useRouter();
    const [data, setData] = useState<AnalysisResponse | null>(null);

    useEffect(() => {
        const stored = sessionStorage.getItem("analysisResult");
        if (stored) {
            try {
                setData(JSON.parse(stored));
            } catch {
                router.push("/analyze");
            }
        } else {
            router.push("/analyze");
        }
    }, [router]);

    if (!data) return <main className={styles.main}><div className="spinner" style={{ margin: "10rem auto" }} /></main>;

    const { apartment, analysis, comparables, negotiation } = data;

    return (
        <main className={styles.main}>
            <div className="container-sm">

                {/* Editorial Header */}
                <header className={styles.header}>
                    <div className={styles.prehead}>Evaluation Report</div>
                    <h1 className="animate-in">{apartment.address}</h1>
                    <div className={`${styles.subtitle} animate-in delay-1`}>
                        A comparative analysis against {analysis.num_comparables} active listings within a 0.5-mile radius.
                    </div>
                </header>

                {/* Executive Summary */}
                <section className={`${styles.section} animate-in delay-2`}>
                    <div className={styles.summaryGrid}>
                        <div className={styles.summaryBlock}>
                            <div className={styles.label}>Current Rent</div>
                            <div className={styles.value}>${apartment.current_rent.toLocaleString()}</div>
                        </div>
                        <div className={styles.summaryBlock}>
                            <div className={styles.label}>Market Estimate</div>
                            <div className={styles.value}>${analysis.market_rate.toLocaleString()}</div>
                        </div>
                        <div className={styles.summaryBlock}>
                            <div className={styles.label}>Variance</div>
                            <div className={styles.value} style={{ color: analysis.is_overpaying ? "var(--status-danger)" : "var(--status-success)" }}>
                                {analysis.is_overpaying ? '+' : ''}${Math.abs(analysis.difference).toLocaleString()}
                            </div>
                        </div>
                    </div>
                </section>

                {/* Narrative Strategy */}
                {negotiation && (
                    <section className={`${styles.section} animate-in delay-3`}>
                        <h2 className={styles.sectionTitle}>Strategic Brief</h2>
                        <div className={styles.prose}>
                            <p>
                                Based on current market conditions, your unit is valued at roughly <strong>${analysis.market_rate.toLocaleString()}</strong> per month.
                                {analysis.is_overpaying
                                    ? ` This indicates you are currently paying a premium of ${analysis.difference_percent.toFixed(1)}% above market rate.`
                                    : " Your current rate is aligned with or below market."}
                            </p>
                            <br />
                            <p><strong>Timing Recommendation:</strong> {negotiation.timing_advice.optimal_window}</p>
                            <ul className={styles.list}>
                                {negotiation.key_data_points.map((pt, i) => <li key={i}>{pt}</li>)}
                            </ul>
                        </div>
                    </section>
                )}

                {/* Minimalist Data Table */}
                <section className={`${styles.section} animate-in delay-3`}>
                    <h2 className={styles.sectionTitle}>Comparable Assets</h2>
                    <div className={styles.tableWrapper}>
                        <table className={styles.dataTable}>
                            <thead>
                                <tr>
                                    <th>Address</th>
                                    <th>Specs</th>
                                    <th>Listed Rent</th>
                                    <th>Adj. Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                {comparables.sort((a, b) => (a.adjusted_rent || a.rent) - (b.adjusted_rent || b.rent)).map((comp, i) => (
                                    <tr key={i}>
                                        <td>{comp.address.split(',')[0]}</td>
                                        <td className="text-muted">{comp.bedrooms}B / {comp.bathrooms}b</td>
                                        <td>${comp.rent.toLocaleString()}</td>
                                        <td><strong>${(comp.adjusted_rent || comp.rent).toLocaleString()}</strong></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* Written Communication */}
                {negotiation && (
                    <section className={`${styles.section} animate-in delay-3`}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "2rem" }}>
                            <h2 className={styles.sectionTitle} style={{ margin: 0, border: "none" }}>Drafted Communication</h2>
                            <button className="btn btn-secondary btn-sm" onClick={() => navigator.clipboard.writeText(negotiation.email_body)}>
                                Copy Draft
                            </button>
                        </div>

                        <div className={styles.letterBox}>
                            <div style={{ paddingBottom: "1.5rem", marginBottom: "1.5rem", borderBottom: "1px solid var(--border-subtle)" }}>
                                <strong style={{ fontFamily: "var(--font-sans)", fontSize: "0.85rem", textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-muted)" }}>Subject</strong><br />
                                <span style={{ fontSize: "1.1rem" }}>{negotiation.email_subject}</span>
                            </div>
                            <div className={styles.letterContent}>
                                {negotiation.email_body}
                            </div>
                        </div>
                    </section>
                )}

            </div>
        </main>
    );
}
