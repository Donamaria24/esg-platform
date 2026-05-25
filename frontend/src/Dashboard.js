import { useEffect, useState } from "react";

import axios from "axios";

import "./Dashboard.css";

function Dashboard() {

    const [summary, setSummary] = useState({});
    const [file, setFile] = useState(null);

    useEffect(() => {

        fetchSummary();

    }, []);

    // FETCH SUMMARY DATA

    const fetchSummary = async () => {

        try {

            const token =
                localStorage.getItem("access");

            const response = await axios.get(

                "http://127.0.0.1:8000/api/emissions/summary/",

                {
                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

            setSummary(response.data);

        } catch (error) {

            console.log(error);
        }
    };

    // CSV UPLOAD

    const uploadCSV = async () => {

        if (!file) {

            alert("Please choose CSV file");

            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        try {

            await axios.post(

                "http://127.0.0.1:8000/api/upload/sap/",

                formData,

                {
                    headers: {
                        "Content-Type":
                            "multipart/form-data"
                    }
                }
            );

            alert("CSV Uploaded Successfully");

            fetchSummary();

        } catch (error) {

            console.log(error);

            alert("Upload Failed");
        }
    };

    // PDF DOWNLOAD

    const downloadPDF = () => {

        window.open(
            "http://127.0.0.1:8000/api/emissions/export/pdf/"
        );
    };

    // LOGOUT

    const logout = () => {

        localStorage.removeItem("access");

        window.location.href = "/";
    };

    return (

        <div className="dashboard">

            {/* TITLE */}

            <h1 className="dashboard-title">
                ESG Emissions Dashboard
            </h1>

            {/* KPI CARDS */}

            <div className="cards">

                <div className="card">

                    <h2>Total Records</h2>

                    <p>
                        {summary.total_records || 0}
                    </p>

                </div>

                <div className="card">

                    <h2>Suspicious Records</h2>

                    <p>
                        {summary.suspicious_records || 0}
                    </p>

                </div>

                <div className="card">

                    <h2>Total Emissions</h2>

                    <p>
                        {summary.total_emissions || 0}
                    </p>

                </div>

            </div>

            {/* CSV UPLOAD */}

            <div className="upload-box">

                <h2>
                    Upload SAP CSV
                </h2>

                <input
                    type="file"
                    onChange={(e) =>
                        setFile(e.target.files[0])
                    }
                />

                <br />
                <br />

                <button
                    className="download-btn"
                    onClick={uploadCSV}
                >
                    Upload CSV
                </button>

            </div>

            {/* ACTION BUTTONS */}

            <div
                style={{
                    marginTop: "30px",
                    display: "flex",
                    gap: "20px"
                }}
            >

                <button
                    className="download-btn"
                    onClick={downloadPDF}
                >
                    Download ESG Report
                </button>

                <button
                    className="download-btn"
                    onClick={logout}
                >
                    Logout
                </button>

            </div>

            {/* LATEST RECORDS */}

            <div
                style={{
                    marginTop: "50px"
                }}
            >

                <h2 className="section-title">
                    Latest Emission Records
                </h2>

                <table
                    style={{
                        width: "100%",
                        borderCollapse: "collapse",
                        background: "#1e293b",
                        color: "white"
                    }}
                >

                    <thead>

                        <tr>

                            <th
                                style={{
                                    padding: "15px",
                                    borderBottom:
                                        "1px solid gray"
                                }}
                            >
                                Activity
                            </th>

                            <th
                                style={{
                                    padding: "15px",
                                    borderBottom:
                                        "1px solid gray"
                                }}
                            >
                                Value
                            </th>

                            <th
                                style={{
                                    padding: "15px",
                                    borderBottom:
                                        "1px solid gray"
                                }}
                            >
                                Unit
                            </th>

                            <th
                                style={{
                                    padding: "15px",
                                    borderBottom:
                                        "1px solid gray"
                                }}
                            >
                                Emission
                            </th>

                            <th
                                style={{
                                    padding: "15px",
                                    borderBottom:
                                        "1px solid gray"
                                }}
                            >
                                Status
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {
                            summary.latest_records &&
                            summary.latest_records.map(
                                (record, index) => (

                                <tr
                                    key={index}
                                >

                                    <td
                                        style={{
                                            padding: "15px"
                                        }}
                                    >
                                        {record.activity_type}
                                    </td>

                                    <td
                                        style={{
                                            padding: "15px"
                                        }}
                                    >
                                        {record.value}
                                    </td>

                                    <td
                                        style={{
                                            padding: "15px"
                                        }}
                                    >
                                        {record.unit}
                                    </td>

                                    <td
                                        style={{
                                            padding: "15px"
                                        }}
                                    >
                                        {record.emission}
                                    </td>

                                    <td
                                        style={{
                                            padding: "15px",
                                            color:
                                                record.suspicious
                                                ? "red"
                                                : "lightgreen"
                                        }}
                                    >
                                        {
                                            record.suspicious
                                            ? "Suspicious"
                                            : "Normal"
                                        }
                                    </td>

                                </tr>
                            ))
                        }

                    </tbody>

                </table>

            </div>

        </div>
    );
}

export default Dashboard;