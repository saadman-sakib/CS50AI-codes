from model import model

# Calculate probability for a given observation
probability = model.probability([["none", "no", "on time", "attend"]])

# probability = model.([["none", "attend"]])

print(probability)
