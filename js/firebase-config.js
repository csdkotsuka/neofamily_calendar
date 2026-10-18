/**
 * Firebase Configuration & Firestore Loader
 * 
 * 1. Cloudflare Pages の環境変数（/api/config）がある場合は自動で読み込みます。
 * 2. ない場合は下記の FIREBASE_CONFIG の値を使用します。
 * 3. いずれも未設定の場合はローカルの events-data.js (INITIAL_EVENTS) で動作します。
 */

let FIREBASE_CONFIG = {
  apiKey: "",             // 例: "AIzaSy..."
  authDomain: "",         // 例: "your-project.firebaseapp.com"
  projectId: "",          // 例: "your-project"
  storageBucket: "",      // 例: "your-project.appspot.com"
  messagingSenderId: "",  // 例: "1234567890"
  appId: ""               // 例: "1:1234567890:web:abcdef..."
};

// Cloudflare Pages の /api/config から環境変数を取得
async function loadConfigFromCloudflare() {
  try {
    const res = await fetch("/api/config");
    if (res.ok) {
      const data = await res.json();
      if (data.apiKey && data.projectId) {
        FIREBASE_CONFIG = {
          apiKey: data.apiKey,
          authDomain: data.authDomain,
          projectId: data.projectId,
          storageBucket: data.storageBucket,
          messagingSenderId: data.messagingSenderId,
          appId: data.appId
        };
        console.log("[NEO FAMILY] Loaded Firebase config from Cloudflare environment variables.");
        return true;
      }
    }
  } catch (e) {
    // Local static server or file preview
  }
  return false;
}

// Check if Firebase is configured
function isFirebaseConfigured() {
  return !!(FIREBASE_CONFIG.apiKey && FIREBASE_CONFIG.projectId);
}

// Load events from Firestore if configured, otherwise fallback to local INITIAL_EVENTS
async function fetchEventsFromFirestore() {
  await loadConfigFromCloudflare();

  if (!isFirebaseConfigured() || typeof firebase === "undefined") {
    console.log("[NEO FAMILY] Using local events dataset.");
    return null;
  }

  try {
    if (!firebase.apps.length) {
      firebase.initializeApp(FIREBASE_CONFIG);
    }
    const db = firebase.firestore();
    const snapshot = await db.collection("events").orderBy("startDate").get();
    
    if (snapshot.empty) {
      console.warn("[NEO FAMILY] Firestore collection 'events' is empty. Falling back to local data.");
      return null;
    }

    const events = [];
    snapshot.forEach(doc => {
      events.push({ id: doc.id, ...doc.data() });
    });

    console.log(`[NEO FAMILY] Successfully loaded ${events.length} events from Firebase Firestore.`);
    return events;
  } catch (err) {
    console.error("[NEO FAMILY] Failed to load events from Firestore:", err);
    return null;
  }
}

// Save or Update an event in Firestore
async function saveEventToFirestore(eventData) {
  if (!isFirebaseConfigured() || typeof firebase === "undefined") {
    return false;
  }
  try {
    if (!firebase.apps.length) {
      firebase.initializeApp(FIREBASE_CONFIG);
    }
    const db = firebase.firestore();
    await db.collection("events").doc(eventData.id).set(eventData, { merge: true });
    console.log(`[NEO FAMILY] Event ${eventData.id} saved to Firestore successfully.`);
    return true;
  } catch (err) {
    console.error("[NEO FAMILY] Failed to save event to Firestore:", err);
    throw err;
  }
}
