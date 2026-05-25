import { useState } from "react";

import axios from "axios";

import "./Login.css";

function Login() {

    const [username, setUsername] =
        useState("");

    const [password, setPassword] =
        useState("");

    const loginUser = async () => {

        try {

            const response =
                await axios.post(

                    "http://127.0.0.1:8000/api/token/",

                    {
                        username,
                        password,
                    }
                );

            localStorage.setItem(
                "access",
                response.data.access
            );

            window.location.reload();

        } catch (error) {

            alert("Invalid credentials");
        }
    };

    return (

        <div className="login-container">

            <div className="login-box">

                <h1 className="login-title">
                    ESG Login
                </h1>

                <input
                    className="login-input"
                    type="text"
                    placeholder="Username"
                    onChange={(e) =>
                        setUsername(e.target.value)
                    }
                />

                <input
                    className="login-input"
                    type="password"
                    placeholder="Password"
                    onChange={(e) =>
                        setPassword(e.target.value)
                    }
                />

                <button
                    className="login-button"
                    onClick={loginUser}
                >
                    Login
                </button>

            </div>

        </div>
    );
}

export default Login;