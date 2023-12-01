package com.smartcontracts.service.impl;

import java.security.SecureRandom;


import org.springframework.stereotype.Service;

import com.smartcontracts.project.model.RandomNumber;
import com.smartcontracts.service.RandomService;

@Service
public class RandomServiceImpl implements RandomService {
	@Override
	public RandomNumber computeRandom(){
		SecureRandom random= new SecureRandom();
		return new RandomNumber(random);	
		
	}
}
