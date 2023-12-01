package com.smartcontracts.project.controller;

import java.math.BigInteger;
import java.util.Random;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.smartcontracts.project.model.ContractAddress;
import com.smartcontracts.project.model.RandomNumber;


@RestController
@RequestMapping("api")
public class Controller {
	private ContractAddress addressLocal= new ContractAddress("null");
	private ContractAddress  addressRinkeby =new ContractAddress("null");
	
	@GetMapping("/random")
	public ResponseEntity<RandomNumber> getRandomNumber(){
		BigInteger random=new BigInteger(256,new Random()); 
		return new ResponseEntity<RandomNumber>(new RandomNumber(random), HttpStatus.OK);
	}
	
	@GetMapping("/random2")
	public ResponseEntity<RandomNumber> getRandomNumber2(){
		BigInteger random=BigInteger.valueOf(12); 
		return new ResponseEntity<RandomNumber>(new RandomNumber(random), HttpStatus.OK);
	}
	
	@PostMapping("/addressganache")
	public ResponseEntity<String> newLocalAddress(@RequestBody String address) {
		addressLocal= new ContractAddress(address);
		return new ResponseEntity<String>("Ok",HttpStatus.OK);
		
	}
	@PostMapping("/addressrinkeby")
	public ResponseEntity<String> newRinkebyAddress(@RequestBody String address) {
		addressRinkeby= new ContractAddress(address);
		return new ResponseEntity<String>("Ok",HttpStatus.OK);		
	}
	
	
	@GetMapping("/addressganache")
	public ResponseEntity<ContractAddress> getLocalAddress(){
		
		return new ResponseEntity<ContractAddress>(addressLocal, HttpStatus.OK);
	}
	@GetMapping("/addressrinkeby")
	public ResponseEntity<ContractAddress> getRinkebyAddress(){
		return new ResponseEntity<ContractAddress>(addressRinkeby, HttpStatus.OK);
	}
	
	
	 

}
