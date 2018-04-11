//
//  LoginViewController.swift
//  DataShark
//
//  Created by Gokul Swamy on 12/24/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit
import LocalAuthentication
import Locksmith

class LoginViewController: UIViewController {
    
    @IBOutlet weak var usernameField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var signUpButton: UIButton!
    @IBOutlet weak var logInButton: UIButton!
    var address: String = ""
    var userID: String = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        usernameField.roundedCorners(top: true)
        passwordField.roundedCorners(top: false)
        signUpButton.layer.cornerRadius = 20.0
        logInButton.layer.cornerRadius = 20.0
        
        // Hide Until TouchID Fails
        usernameField.isHidden = true
        passwordField.isHidden = true
        passwordField.isSecureTextEntry = true
        signUpButton.isHidden = true
        logInButton.isHidden = true
        
        // Used to move screen up when keyboard is visible
        NotificationCenter.default.addObserver(self, selector: #selector(LoginViewController.keyboardWillShow(sender:)), name: NSNotification.Name.UIKeyboardWillShow, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(LoginViewController.keyboardWillHide(sender:)), name: NSNotification.Name.UIKeyboardWillHide, object: nil)
        
        // Only use TouchID if credentials have been saved
        let dictionary = Locksmith.loadDataForUserAccount(userAccount: "datashark")
        if let credentials = dictionary {
            touchAuth(credentials: credentials)
        }
    }

    
    func touchAuth(credentials: [String: Any]) {
        let context = LAContext()
        if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: nil) {
            context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Use TouchID to login.", reply: { (success, error) in
                DispatchQueue.main.async {
                    if success {
                        // Fill in hidden username/password fields and submit
                        self.usernameField.text = (credentials["email"] as! String)
                        self.passwordField.text = (credentials["password"] as! String)
                        self.logIn(self)
                    } else {
                        // Show username/password fields
                        self.usernameField.isHidden = false
                        self.passwordField.isHidden = false
                        self.signUpButton.isHidden = false
                        self.logInButton.isHidden = false
                    }
                }
            })
        }
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        // Tap to dismiss keyboard
        self.view.endEditing(true)
    }
    
    @objc func keyboardWillShow(sender: NSNotification) {
        // Move fields up when keyboard appears
        self.view.frame.origin.y = -200
    }
    
    @objc func keyboardWillHide(sender: NSNotification) {
        // Move fields down when keyboard disappears
        self.view.frame.origin.y = 0
    }
    
    @IBAction func signUp(_ sender: Any) {
        self.view.endEditing(true)
        let email = usernameField.text
        let password = passwordField.text
        let body = ["email": email ?? "", "password": password ?? "", "datasets": ""]
        do{
            let json = try (JSONSerialization.data(withJSONObject: body, options: JSONSerialization.WritingOptions.prettyPrinted))
            var request = URLRequest(url: URL(string:"https://dataagora.com/createUser")!)
            request.httpMethod = "POST"
            request.httpBody = json
            URLSession.shared.dataTask(with: request) { data, response, error in
                if error != nil {
                    //Error Handling
                    let alertController = UIAlertController(title: "Could Not Sign Up", message: "Sorry, but we were unable to sign you up for DataAgora. Please try again a little bit later.", preferredStyle: .alert)
                    alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alertController, animated: true, completion: nil)
                } else {
                    //TODO: Onboarding
                    let alertController = UIAlertController(title: "To Be Implemented", message: "Will be implemented in a future version.", preferredStyle: .alert)
                    alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alertController, animated: true, completion: nil)
                }
                }.resume()
        }
        catch {
            print("incompatable body")
        }
    }
    
    @IBAction func logIn(_ sender: Any) {
        self.view.endEditing(true)
        let email = usernameField.text
        let password = passwordField.text
        let body = ["email": email ?? "", "password": password ?? ""]
        do{
            let json = try (JSONSerialization.data(withJSONObject: body, options: JSONSerialization.WritingOptions.prettyPrinted))
            var request = URLRequest(url: URL(string:"https://dataagora.com/loginUser")!)
            request.httpMethod = "POST"
            request.httpBody = json
            URLSession.shared.dataTask(with: request) { data, response, error in
                if error != nil {
                    //Your HTTP request failed.
                    let alertController = UIAlertController(title: "Could Not Log In", message: "Sorry, but we were unable to log you into DataAgora. Please try again a little bit later.", preferredStyle: .alert)
                    alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alertController, animated: true, completion: nil)
                } else {
                    do {
                        // Save password if not saved already
                        let dictionary = Locksmith.loadDataForUserAccount(userAccount: "datashark")
                        if dictionary == nil {
                            try Locksmith.saveData(data: ["email": email ?? "", "password": password ?? ""], forUserAccount: "datashark")
                        } else {
                            try Locksmith.updateData(data: ["email": email ?? "", "password": password ?? ""], forUserAccount: "datashark")
                        }
                        
                    } catch {
                        // Do Nothing
                    }
                    if let data = data {
                        do {
                            let serialized = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                            if let response = serialized, let address = response["address"], let userID = response["userID"] {
                                self.address = String(describing: address)
                                self.userID = String(describing: userID)
                            }
                        } catch {
                            
                        }
                    }
                    self.performSegue(withIdentifier: "loginToMain", sender: nil)
                    //Your HTTP request succeeded
                }
                }.resume()
        }
        catch {
            print("incompatable body")
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Passing Data
        if segue.identifier == "loginToMain" {
            if let destinationVC = segue.destination as? MainViewController{
                destinationVC.address = self.address
                destinationVC.userID = self.userID
            }
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
