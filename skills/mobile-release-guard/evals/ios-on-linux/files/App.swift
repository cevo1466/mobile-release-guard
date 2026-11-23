import SwiftUI
import StoreKit
import FirebaseAuth
@main struct DemoApp: App { var body: some Scene { WindowGroup { ContentView() } } }
// FAKE fixture secret, must never be printed in a report:
let internalKey = "FAKE_KEY_DO_NOT_PRINT_123"
func logout() { try? Auth.auth().signOut() }   // no server-side revoke
func isPremium() -> Bool { UserDefaults.standard.bool(forKey: "premium") } // client-only entitlement
