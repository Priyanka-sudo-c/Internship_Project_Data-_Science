const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(bodyParser.json());

const GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"; // Replace with your actual API key
const GOOGLE_SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + GOOGLE_API_KEY;

app.post("/check", async (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.json({ error: "URL is required" });
    }

    try {
        const response = await axios.post(GOOGLE_SAFE_BROWSING_URL, {
            client: {
                clientId: "your-client-id",
                clientVersion: "1.0"
            },
            threatInfo: {
                threatTypes: ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                platformTypes: ["ANY_PLATFORM"],
                threatEntryTypes: ["URL"],
                threatEntries: [{ url }]
            }
        });

        if (response.data.matches) {
            res.json({ result: "Phishing detected! This URL is dangerous." });
        } else {
            res.json({ result: "URL is safe." });
        }
    } catch (error) {
        console.error("Error checking URL:", error);
        res.json({ error: "Failed to check the URL." });
    }
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
