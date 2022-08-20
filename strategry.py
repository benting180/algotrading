class CrossExchangeMarketMaker:
    def __init__(self, symbol_pair, min_prof):
        self.symbol_pair = symbol_pair
        self.min_prof = min_prof

    def calculate_maker_order(self, tick):
        # @TODO: the tick unpacking step can be placed somewhere else
        best_bid_price = float(tick['bestBid'])
        best_bid_size = float(tick['bestBidSize'])
        best_ask_price = float(tick['bestAsk'])
        best_ask_size = float(tick['bestAskSize'])

        # calculation
        bid_price = best_bid_price * (1 - self.min_prof)
        ask_price = best_ask_price * (1 + self.min_prof)
        bid_size = best_bid_size
        ask_size = best_ask_size
        buy = {'price': bid_price, 'size': bid_size}
        sell = {'price': ask_price, 'size': ask_size}
        return buy, sell

    def calculate_taker_order(self, tick):
        best_bid_price = float(tick['bestBid'])
        best_bid_size = float(tick['bestBidSize'])
        best_ask_price = float(tick['bestAsk'])
        best_ask_size = float(tick['bestAskSize'])
        ask = {'price': best_bid_price, 'size': best_bid_size} 
        bid = {'price': best_ask_price, 'size': best_ask_size}
        return bid, ask
    
    def set_min_prof(self, min_prof):
        # @TODO: check min_prof within acceptable value
        self.min_prof = min_prof
        

