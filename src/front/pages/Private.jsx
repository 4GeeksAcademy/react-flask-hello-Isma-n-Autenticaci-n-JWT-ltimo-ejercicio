import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Private = () => {
    const { store, dispatch } = useGlobalReducer();
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const validateToken = async () => {
            const token = store.token;

            if (!token) {
                navigate("/login");
                return;
            }

            try {
                const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/token/validate`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Token validation failed");
                }

                const data = await response.json();
                dispatch({ type: "set_user", payload: data.user });
                setLoading(false);
            } catch (error) {
                dispatch({ type: "logout" });
                navigate("/login");
            }
        };

        validateToken();
    }, []);

    const handleLogout = () => {
        dispatch({ type: "logout" });
        navigate("/login");
    };

    if (loading) {
        return (
            <div className="container mt-5 text-center">
                <div className="spinner-border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="card-title">Private Page</h2>
                            <p className="card-text">
                                Welcome! You are authenticated.
                            </p>
                            {store.user && (
                                <div className="alert alert-info">
                                    <strong>User Email:</strong> {store.user.email}
                                    <br />
                                    <strong>User ID:</strong> {store.user.id}
                                </div>
                            )}
                            <button
                                className="btn btn-danger"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};