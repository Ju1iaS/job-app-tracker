const API_BASE = 'http://127.0.0.1:8000';

export async function login(email, password) {
    const res = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Login failed');
    }
    return res.json();
}

export async function signup(email, password) {
    const res = await fetch(`${API_BASE}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password})
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Signup failed');
    }
    return res.json();
}

export async function getApplications(token) {
    const res = await fetch(`${API_BASE}/applications`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not load applications');
    }
    return res.json();
}

export async function createApplication(token, applicationData) {
    const res = await fetch(`${API_BASE}/applications`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(applicationData),
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not create application');
    }
    return res.json();
}

export async function updateApplication(token, applicationId, updates) {
    const res = await fetch(`${API_BASE}/applications/${applicationId}`, {
        method: 'PATCH',
        headers: { 
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updates),
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not update application');
    }
    return res.json();
}

export async function deleteApplication(token, applicationId) {
    const res = await fetch(`${API_BASE}/applications/${applicationId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}`},
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not delete application');
    }
    return res.json();
}

export async function getFunnel(token) {
    const res = await fetch(`${API_BASE}/summary/funnel`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not load funnel data');
    }
    return res.json();
}

export async function getResponseTime(token) {
    const res = await fetch(`${API_BASE}/summary/response-time`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not load response time data');
    }
    return res.json();
}

export async function getByGroup(token, groupBy = 'source') {
    const res = await fetch(`${API_BASE}/summary/by-group?group_by=${groupBy}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Could not load breakdown');
    }
    return res.json();
}


