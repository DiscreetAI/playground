//
//  AuthViewController.swift
//  DataShark
//
//  Created by Gokul Swamy on 12/26/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit
import OAuthSwift

class AuthViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    
    @IBOutlet weak var tableView: UITableView!
    var userID: String = ""
    var address: String = ""
    var serviceName: String  = ""
    var scopes: [String] = []
    var selected: [Bool] = []
    var serviceToURL: [String: String] = ["uber": "https://login.uber.com/oauth/v2/authorize",
                                             "fitbit": "https://www.fitbit.com/oauth2/authorize",
                                             "lyft": "https://api.lyft.com/oauth/authorize"]
    var serviceToSecret: [String: String] = ["uber": "J7vY3yBGZr19EIrtibQZPhJm2qPulKy-Zs2VMMQz",
                                             "fitbit": "92ef15bf527e8c3684ff6f54517d235e",
                                             "lyft": "ve3ul8VMMiiQ7zrft33S2gzAy8258436"]
    var serviceToKey: [String: String] = ["uber": "cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K",
                                          "fitbit": "22CH8Y",
                                          "lyft": "xWcQoJgCDyyx"]

    override func viewDidLoad() {
        super.viewDidLoad()
        
        tableView.dataSource = self
        tableView.delegate = self
        tableView.backgroundColor = .clear
        
        for _ in scopes {
            selected.append(false)
        }
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return scopes.count
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        if let cell = tableView.cellForRow(at: indexPath as IndexPath) { // Flipping selection
            if cell.accessoryType == .checkmark{
                cell.accessoryType = .none
                selected[indexPath.row] = false
            }
            else{
                cell.accessoryType = .checkmark
                selected[indexPath.row] = true
            }
        }
        
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "authCell", for: indexPath)
        cell.textLabel?.text = scopes[indexPath.row]
        cell.textLabel?.textColor = .white
        
        let bgColorView = UIView()
        bgColorView.backgroundColor = #colorLiteral(red: 0.1098039216, green: 0.7568627451, blue: 0.7568627451, alpha: 1)
        cell.selectedBackgroundView = bgColorView
        
        return cell
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func backButtonPressed(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
    
    @IBAction func nextButtonPressed(_ sender: Any) {
        // https://github.com/OAuthSwift/OAuthSwift/blob/master/Demo/Common/ViewController.swift
//         This is just a skeleton - implement on a per-service basis
        let sn = serviceName.lowercased()
        let selectedScopes = zip(selected, scopes).filter { $0.0 }.map { $1 }
        let oauthswift = OAuth2Swift(
            consumerKey:    serviceToKey[sn]!,
            consumerSecret: serviceToSecret[sn]!,
            authorizeUrl:   serviceToURL[sn]!,
            responseType:   "token"
        )

        oauthswift.authorizeURLHandler = SafariURLHandler(viewController: self, oauthSwift: oauthswift)
        // Usually, callback URL of the form URL(string: "datashark://oauth-callback/" + sn)!
        oauthswift.authorize(
            withCallbackURL: URL(string: "https://dataagora.com")!,
            scope: selectedScopes.joined(separator: "+"), state: sn.uppercased(),
            success: { credential, response, parameters in
                let token = credential.oauthToken
                let refreshToken = credential.oauthRefreshToken
                let body = ["authToken": token, "refreshToken": refreshToken]
                do{
                    let json = try (JSONSerialization.data(withJSONObject: body, options: JSONSerialization.WritingOptions.prettyPrinted))
                    var request = URLRequest(url: URL(string:"https://dataagora.com/insert/" + self.serviceName)!)
                    request.httpMethod = "POST"
                    request.httpBody = json
                    URLSession.shared.dataTask(with: request) { data, response, error in
                        if error != nil {
                            //Error Handling
                            let alertController = UIAlertController(title: "Could Not Authenticate", message: "Sorry, we were not able to authenticate your chosen service. Please try again later.", preferredStyle: .alert)
                            alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                            self.present(alertController, animated: true, completion: nil)
                        } else {
                            // Take user back to refreshed main screen
                            let storyboard = UIStoryboard(name: "Main", bundle: nil)
                            let controller = storyboard.instantiateViewController(withIdentifier: "mainVC")
                            self.present(controller, animated: true, completion: nil)
                        }
                        }.resume()
                }
                catch {
                    print("incompatable body")
                }
        },
            failure: { error in
                let alertController = UIAlertController(title: "Could Not Authenticate", message: "Sorry, we were not able to authenticate your chosen service. Please try again later.", preferredStyle: .alert)
                alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                self.present(alertController, animated: true, completion: nil)
        }
        )
    }
    

}
