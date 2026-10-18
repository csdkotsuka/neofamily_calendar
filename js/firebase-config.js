/**
 * Firebase Configuration & Firestore Loader
 * 
 * Firebase Console (https://console.firebase.google.com/) で取得した
 * firebaseConfig を以下に貼り付けることで、Firestore / Firebase Storage と自動連携します。
 * 設定が空の場合はローカルの events-data.js (INITIAL_EVENTS) を使用してフォールバック動作します。
 */

const FIREBASE_CONFIG = {
  apiKey: "",             // 例: "AIzaSy..."
  authDomain: "",         // 例: "your-project.firebaseapp.com"
  projectId: "",          // 例: "your-project"
  storageBucket: "",      // 例: "your-project.appspot.com"
  messagingSenderId: "",  // 例: "1234567890"
  appId: ""               // 例: "1:1234567890:web:abcdef..."
};

// Check if Firebase is configured
function isFirebaseConfigured() {
  return FIREBASE_CONFIG.apiKey && FIREBASE_CONFIG.projectId;
}

// Load events from Firestore if configured, otherwise fallback to local INITIAL_EVENTS
async function fetchEventsFromFirestore() {
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
