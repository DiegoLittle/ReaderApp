//
//  SignInWithAppleDelegates.swift
//  ReaderApp
//
//  Created by Diego Little on 4/29/22.
//

import UIKit
import AuthenticationServices
import Contacts

class SignInWithAppleDelegates: NSObject {
  private let signInSucceeded: (Bool) -> Void
  private weak var window: UIWindow!
  
  init(window: UIWindow?, onSignedIn: @escaping (Bool) -> Void) {
    self.window = window
    self.signInSucceeded = onSignedIn
  }
}

extension SignInWithAppleDelegates: ASAuthorizationControllerDelegate {
  private func registerNewAccount(credential: ASAuthorizationAppleIDCredential) {
    // 1
    let userData = UserData(email: credential.email!,
                            name: credential.fullName!,
                            identifier: credential.user)

    // 2
    let keychain = UserDataKeychain()
    do {
      try keychain.store(userData)
    } catch {
      self.signInSucceeded(false)
    }

    // 3
    do {
      let success = try WebApi.Register(user: userData,
                                        identityToken: credential.identityToken,
                                        authorizationCode: credential.authorizationCode)
      self.signInSucceeded(success)
    } catch {
      self.signInSucceeded(false)
    }
  }

  private func signInWithExistingAccount(credential: ASAuthorizationAppleIDCredential) {
    // You *should* have a fully registered account here.  If you get back an error from your server
    // that the account doesn't exist, you can look in the keychain for the credentials and rerun setup
      var identityToken = String(data: credential.identityToken!, encoding: .utf8)!
      var authorizationCode = String(data: credential.authorizationCode!, encoding: .utf8)!
//      WebApi.SignIn(credential:)
      let keychain = UserDataKeychain()
      do{
          let retrieved = try keychain.retrieve()
          print(retrieved)

      }
      catch{
          print(error)
      }
      do {
        let success = try WebApi.SignIn(user_id:credential.user, identityToken:identityToken, authorizationCode:authorizationCode)
        self.signInSucceeded(success)
      } catch {
        self.signInSucceeded(false)
      }
  }

  private func signInWithUserAndPassword(credential: ASPasswordCredential) {
    // You *should* have a fully registered account here.  If you get back an error from your server
    // that the account doesn't exist, you can look in the keychain for the credentials and rerun setup

    // if (WebAPI.Login(credential.user, credential.password)) {
    //   ...
    // }
    self.signInSucceeded(true)
  }
  
  func authorizationController(controller: ASAuthorizationController, didCompleteWithAuthorization authorization: ASAuthorization) {
    switch authorization.credential {
    case let appleIdCredential as ASAuthorizationAppleIDCredential:
      if let _ = appleIdCredential.email, let _ = appleIdCredential.fullName {
        registerNewAccount(credential: appleIdCredential)
      } else {
        signInWithExistingAccount(credential: appleIdCredential)
      }

      break
      
    case let passwordCredential as ASPasswordCredential:
      signInWithUserAndPassword(credential: passwordCredential)

      break
      
    default:
      break
    }
  }
  
  func authorizationController(controller: ASAuthorizationController, didCompleteWithError error: Error) {
    // Handle error.
  }
}

extension SignInWithAppleDelegates: ASAuthorizationControllerPresentationContextProviding {
  func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
    return self.window
  }
}
