import SwiftUI
import StoreKit
// client calls LLM directly
let url = URL(string: "https://api.openai.com/v1/chat/completions")!
let apiKey = "FAKE_LLM_KEY_DO_NOT_PRINT_456"
let plus = UserDefaults.standard.bool(forKey: "plus")
