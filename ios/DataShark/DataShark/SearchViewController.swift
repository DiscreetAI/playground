//
//  SearchViewController.swift
//  DataShark
//
//  Created by Gokul Swamy on 12/26/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit

class NewServiceCell: UITableViewCell {
    @IBOutlet weak var serviceIcon: UIImageView!
    @IBOutlet weak var serviceName: UILabel!
    @IBOutlet weak var serviceScopes: UILabel!
    
}

class SearchViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UISearchResultsUpdating {
    
    @IBOutlet weak var tableView: UITableView!
    var userID: String = ""
    var address: String = ""
    var serviceNames: [String] = []
    var filteredServiceNames: [String] = []
    var activeServiceNames: [String] = []
    var serviceScopes: [String: String] = [:]
    let nameToLogo: [String: UIImage] = ["fitbit": #imageLiteral(resourceName: "Fitbit"), "uber": #imageLiteral(resourceName: "Uber"), "lyft": #imageLiteral(resourceName: "Lyft")] // Needs to be updated when new services added
    var searchController: UISearchController!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.delegate = self
        tableView.dataSource = self
        tableView.backgroundColor = .clear
        
        searchController = UISearchController(searchResultsController: nil)
        searchController.searchResultsUpdater = self
        searchController.dimsBackgroundDuringPresentation = false
        searchController.searchBar.sizeToFit()
        searchController.searchBar.barTintColor = #colorLiteral(red: 0.1821299195, green: 0.2213197649, blue: 0.3193987012, alpha: 1)
        tableView.tableHeaderView = searchController.searchBar
        definesPresentationContext = true

        // Preloading scopes
        var request = URLRequest(url: URL(string:"http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/allServices")!)
        request.httpMethod = "GET"
        URLSession.shared.dataTask(with: request) { data, response, error in
            if error == nil {
                if let data = data {
                    do {
                        let serialized = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                        if let response = serialized{
                            let allServices = Set(response.keys)
                            self.serviceNames = Array(allServices.subtracting(Set(self.activeServiceNames))).sorted()
                            self.filteredServiceNames = self.serviceNames
                            for name in self.serviceNames {
                                self.serviceScopes[name] = String(describing: response[name]!)
                            }
                            DispatchQueue.main.async {
                                self.tableView.reloadData()
                            }
                        }
                    } catch {
                        
                    }
                }
            }
            }.resume()
        // Do any additional setup after loading the view.
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        self.performSegue(withIdentifier: "searchToAuth", sender: indexPath)
    }
    
    func updateSearchResults(for searchController: UISearchController) {
        // Filtering rows
        if let searchText = searchController.searchBar.text {
                        filteredServiceNames = searchText.isEmpty ? serviceNames : serviceNames.filter({(dataString: String) -> Bool in
                            return dataString.range(of: searchText, options: .caseInsensitive) != nil
                        })
            
            tableView.reloadData()
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return filteredServiceNames.count
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "newServiceCell", for: indexPath) as! NewServiceCell
        cell.serviceName.text = filteredServiceNames[indexPath.row]
        cell.serviceScopes.text = serviceScopes[filteredServiceNames[indexPath.row]]
        
        if (nameToLogo.keys.contains(filteredServiceNames[indexPath.row].lowercased())) {
            cell.serviceIcon.image = self.nameToLogo[filteredServiceNames[indexPath.row].lowercased()]
        } else {
            cell.serviceIcon.image = #imageLiteral(resourceName: "Unknown")
        }
        // Rounding corners
        cell.serviceIcon.translatesAutoresizingMaskIntoConstraints = false
        cell.serviceIcon.addConstraint(NSLayoutConstraint(item: cell.serviceIcon,
                                                          attribute: NSLayoutAttribute.height,
                                                          relatedBy: NSLayoutRelation.equal,
                                                          toItem: cell.serviceIcon,
                                                          attribute: NSLayoutAttribute.width,
                                                          multiplier: 1,
                                                          constant: 0))
        cell.serviceIcon.clipsToBounds = true
        cell.serviceIcon.layer.cornerRadius = 22
        
        let bgColorView = UIView()
        bgColorView.backgroundColor = #colorLiteral(red: 0.1098039216, green: 0.7568627451, blue: 0.7568627451, alpha: 1)
        cell.selectedBackgroundView = bgColorView
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 100.0
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "searchToAuth" {
            if let destinationVC = segue.destination as? AuthViewController{
                let idx = sender as! IndexPath
                destinationVC.address = self.address
                destinationVC.userID = self.userID
                destinationVC.serviceName = self.filteredServiceNames[idx.row]
                destinationVC.scopes = (self.serviceScopes[self.filteredServiceNames[idx.row]]?.components(separatedBy: ", "))!
            }
        }
    }
    
    @IBAction func doneButtonPressed(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
    

}
