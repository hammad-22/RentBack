"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { analyzeApartment, ApartmentInput } from "@/lib/api";
import styles from "./analyze.module.css";

const AMENITIES_OPTIONS = [
    "Doorman", "Elevator", "Laundry In-Unit", "Laundry In Building",
    "Dishwasher", "Central AC", "Gym", "Roof Deck", "Pet Friendly",
    "Storage", "Bike Room", "Hardwood Floors", "Renovated Kitchen",
    "Natural Light", "City Views", "Balcony", "Outdoor Space", "Concierge",
];

// Address Autocomplete UI
function AddressAutocomplete({
    value,
    onChange,
    onSelectCityZip
}: {
    value: string,
    onChange: (val: string) => void,
    onSelectCityZip: (city: string, zip: string) => void
}) {
    const [query, setQuery] = useState(value);
    const [results, setResults] = useState<any[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);
    const justSelected = useRef(false);
    const wrapperRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // Don't search right after a selection
        if (justSelected.current) {
            justSelected.current = false;
            return;
        }

        if (query.length < 4) {
            setShowDropdown(false);
            return;
        }

        const timeoutId = setTimeout(async () => {
            setIsSearching(true);
            try {
                const res = await fetch(
                    `https://nominatim.openstreetmap.org/search?` +
                    `q=${encodeURIComponent(query + ', New York City, NY')}` +
                    `&format=json&addressdetails=1&limit=5&countrycodes=us`,
                    { headers: { 'Accept': 'application/json' } }
                );
                const data = await res.json();
                setResults(data);
                setShowDropdown(data.length > 0);
            } catch (e) {
                console.error("Geocoding error", e);
            } finally {
                setIsSearching(false);
            }
        }, 400);
        return () => clearTimeout(timeoutId);
    }, [query]);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
                setShowDropdown(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleSelect = (item: any) => {
        justSelected.current = true;
        const addressStr = item.display_name.split(',').slice(0, 2).join(',').trim();
        setQuery(addressStr);
        onChange(addressStr);

        // Attempt to extract postcode and city/borough
        const zip = item.address?.postcode || "";
        let city = item.address?.borough || item.address?.suburb || item.address?.city || "";

        // Normalize to the 5 boroughs for the dropdown
        if (city.includes("Bronx")) city = "Bronx";
        else if (city.includes("Staten")) city = "Staten Island";
        else if (city.includes("Brooklyn") || city.includes("Kings")) city = "Brooklyn";
        else if (city.includes("Queens")) city = "Queens";
        else if (city.includes("Manhattan") || city.includes("New York")) city = "Manhattan";
        else city = ""; // Let user select if unknown

        onSelectCityZip(city, zip);

        setShowDropdown(false);
    };

    return (
        <div className={styles.autocompleteWrapper} ref={wrapperRef}>
            <input
                className="form-input"
                type="text"
                placeholder="Start typing your NYC address..."
                value={query}
                onChange={(e) => {
                    setQuery(e.target.value);
                    onChange(e.target.value);
                }}
                autoFocus
            />
            {isSearching && <div className={styles.searchIndicator}><div className="spinner" style={{ width: 14, height: 14 }} /></div>}

            {showDropdown && results.length > 0 && (
                <ul className={styles.dropdownList}>
                    {results.map((item, idx) => {
                        const displayName = item.display_name.split(',').slice(0, 2).join(', ');
                        const suburb = item.address?.suburb || item.address?.city || item.address?.county || '';
                        return (
                            <li key={idx} onClick={() => handleSelect(item)} className={styles.dropdownItem}>
                                <strong>{displayName}</strong>
                                <span className="text-muted" style={{ marginLeft: "0.5rem", fontSize: "0.85rem" }}>
                                    {suburb ? `${suburb}, NY ` : "NY "}{item.address?.postcode || ''}
                                </span>
                            </li>
                        );
                    })}
                </ul>
            )}
        </div>
    );
}

export default function AnalyzePage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [formData, setFormData] = useState<ApartmentInput>({
        address: "",
        city: "",
        state: "NY",
        zip_code: "",
        bedrooms: 1,
        bathrooms: 1,
        sqft: null,
        floor_level: null,
        current_rent: 0,
        lease_end_date: null,
        amenities: [],
        building_type: null,
        year_built: null,
    });

    const updateField = (field: keyof ApartmentInput, value: unknown) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    const toggleAmenity = (amenity: string) => {
        setFormData((prev) => ({
            ...prev,
            amenities: prev.amenities.includes(amenity)
                ? prev.amenities.filter((a) => a !== amenity)
                : [...prev.amenities, amenity],
        }));
    };

    const handleSubmit = async () => {
        if (!formData.address || formData.current_rent <= 0) {
            setError("Please complete the required location and rent fields.");
            window.scrollTo({ top: 0, behavior: "smooth" });
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const result = await analyzeApartment(formData);
            sessionStorage.setItem("analysisResult", JSON.stringify(result));
            router.push("/results");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Analysis failed.");
            setLoading(false);
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    };

    return (
        <main className={styles.main}>
            <div className="container-sm">

                <div className={styles.header}>
                    <div className={styles.stepIndicator}>Unit Specification</div>
                    <h1 className="animate-in">Provide Your Parameters</h1>
                </div>

                {error && (
                    <div className={`${styles.errorBox} animate-in`}>
                        {error}
                    </div>
                )}

                <div className={`${styles.formSection} animate-in delay-1`}>
                    <h2 className={styles.sectionTitle}>I. Location</h2>
                    <div className="form-group">
                        <label className="form-label">Search Address *</label>
                        <AddressAutocomplete
                            value={formData.address}
                            onChange={(val) => updateField("address", val)}
                            onSelectCityZip={(city, zip) => {
                                updateField("city", city);
                                updateField("zip_code", zip);
                            }}
                        />
                    </div>
                    <div className={styles.formRow}>
                        <div className="form-group">
                            <label className="form-label">Borough</label>
                            <select className="form-select" value={formData.city} onChange={(e) => updateField("city", e.target.value)}>
                                <option value="" disabled>Select borough...</option>
                                <option value="Manhattan">Manhattan</option>
                                <option value="Brooklyn">Brooklyn</option>
                                <option value="Queens">Queens</option>
                                <option value="Bronx">The Bronx</option>
                                <option value="Staten Island">Staten Island</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">ZIP Code</label>
                            <input className="form-input" type="text" value={formData.zip_code} onChange={(e) => updateField("zip_code", e.target.value)} />
                        </div>
                    </div>
                </div>

                <div className={`${styles.formSection} animate-in delay-2`}>
                    <h2 className={styles.sectionTitle}>II. Economics</h2>
                    <div className={styles.formRow}>
                        <div className="form-group">
                            <label className="form-label">Current Monthly Rent ($) *</label>
                            <input
                                className="form-input"
                                type="number"
                                placeholder="e.g. 3500"
                                value={formData.current_rent || ""}
                                onChange={(e) => updateField("current_rent", parseFloat(e.target.value) || 0)}
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Lease End Date</label>
                            <input
                                className="form-input"
                                type="date"
                                value={formData.lease_end_date || ""}
                                onChange={(e) => updateField("lease_end_date", e.target.value)}
                            />
                        </div>
                    </div>
                </div>

                <div className={`${styles.formSection} animate-in delay-3`}>
                    <h2 className={styles.sectionTitle}>III. Physical Attributes</h2>

                    <div className={styles.formRow}>
                        <div className="form-group">
                            <label className="form-label">Bedrooms *</label>
                            <select className="form-select" value={formData.bedrooms} onChange={(e) => updateField("bedrooms", parseInt(e.target.value))}>
                                <option value={0}>Studio</option>
                                <option value={1}>1 Bed</option>
                                <option value={2}>2 Beds</option>
                                <option value={3}>3+ Beds</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Bathrooms *</label>
                            <select className="form-select" value={formData.bathrooms} onChange={(e) => updateField("bathrooms", parseFloat(e.target.value))}>
                                <option value={1}>1.0</option>
                                <option value={1.5}>1.5</option>
                                <option value={2}>2.0</option>
                                <option value={2.5}>2.5+</option>
                            </select>
                        </div>
                    </div>

                    <div className={styles.formRow}>
                        <div className="form-group">
                            <label className="form-label">Square Feet</label>
                            <input className="form-input" type="number" placeholder="Optional" value={formData.sqft || ""} onChange={(e) => updateField("sqft", parseInt(e.target.value))} />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Floor</label>
                            <input className="form-input" type="number" placeholder="Optional" value={formData.floor_level || ""} onChange={(e) => updateField("floor_level", parseInt(e.target.value))} />
                        </div>
                    </div>

                    <div className="form-group" style={{ marginTop: "2rem" }}>
                        <label className="form-label">Select Amenities</label>
                        <div className={styles.amenitiesGrid}>
                            {AMENITIES_OPTIONS.map((a) => (
                                <button
                                    key={a}
                                    className={`${styles.amenityChip} ${formData.amenities.includes(a) ? styles.amenityActive : ""}`}
                                    onClick={() => toggleAmenity(a)}
                                    type="button"
                                >
                                    {a}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                <div className={styles.actions}>
                    <button
                        className="btn btn-primary btn-lg"
                        style={{ width: "100%" }}
                        onClick={handleSubmit}
                        disabled={loading}
                    >
                        {loading ? <div className="spinner" /> : "Generate Report"}
                    </button>
                </div>

            </div>
        </main>
    );
}
