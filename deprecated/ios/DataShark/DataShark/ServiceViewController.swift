//
//  ServiceViewController.swift
//  DataShark
//
//  Created by Gokul Swamy on 12/26/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit

class ServiceViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var disconnectButton: UIButton!
    @IBOutlet weak var profitLabel: UILabel!
    @IBOutlet weak var navBar: UINavigationBar!
    var serviceName: String = ""
    var userID: String = ""
    var address: String = ""
    var serviceProfit: Double = 0.0
    var scopes: [String] = []
    override func viewDidLoad() {
        super.viewDidLoad()
        navBar.topItem?.title = serviceName
        tableView.delegate = self
        tableView.dataSource = self
        tableView.backgroundColor = .clear
        
        DispatchQueue.main.async { // Required for performance
            self.profitLabel.text = "$" + String(self.serviceProfit)
        }
        disconnectButton.layer.cornerRadius = 15.0
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "scopeCell", for: indexPath)
        cell.textLabel?.text = scopes[indexPath.row]
        cell.textLabel?.textColor = .white
        cell.textLabel?.textAlignment = .center
        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return scopes.count
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    @IBAction func doneButtonPressed(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
    
    
    @IBAction func disconnect(_ sender: Any) {
        // Perform a POST request to revoke Auth. Needs to be further customized.
        let body = ["service": serviceName, "userID": userID, "address": address]
        do{
            let json = try (JSONSerialization.data(withJSONObject: body, options: JSONSerialization.WritingOptions.prettyPrinted))
            var request = URLRequest(url: URL(string:"http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/revokeAuth")!)
            request.httpMethod = "POST"
            request.httpBody = json
            URLSession.shared.dataTask(with: request) { data, response, error in
                if error != nil {
                    //Error Handling
                    let alertController = UIAlertController(title: "Could Not Sign Up", message: "Sorry, but we were unable to revoke authorization for this service. Please try again a little bit later or go to the service provider's website.", preferredStyle: .alert)
                    alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alertController, animated: true, completion: nil)
                } else {
                    self.dismiss(animated: true, completion: nil)
                }
                }.resume()
        }
        catch {
            print("incompatable body")
        }
    }
}
